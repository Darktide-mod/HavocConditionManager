"""Run this project's checks; --only reports an explicit selected subset."""
from pathlib import Path
import argparse
import hashlib, json, os, subprocess, sys, time
TESTS=Path(__file__).resolve().parent
PROJECT=TESTS.parent
CHECKS=PROJECT/'build/checks'
CHECKS.mkdir(parents=True,exist_ok=True)
environment=dict(os.environ, PYTHONIOENCODING='utf-8')
CASES = [
    'syntax_tests.py', 'game_1_13_compat_tests.py', 'native_replacement_loading_tests.py',
    'custom_havoc_rank_tests.py', 'custom_efl_tests.py', 'dropdown_visibility_tests.py', 'suite_evidence_tests.py',
    'filesystem_ffi_tests.py', 'diy_minion_lifecycle_tests.py', 'minion_stat_gate_tests.py', 'native_template_tests.py',
    'native_intensity_profile_tests.py', 'native_elite_balance_tests.py', 'native_coordinated_load_tests.py',
    'native_runtime_tests.py', 'native_pressure_tests.py', 'native_encounter_location_tests.py',
    'native_reachable_placement_tests.py', 'native_door_placement_tests.py', 'native_special_pressure_tests.py',
    'native_roamer_memory_tests.py', 'native_spawn_integrity_tests.py', 'native_spawn_smoothing_tests.py',
    'native_straggler_tests.py', 'native_rear_ambient_tests.py', 'native_refill_optimization_tests.py',
    'native_recycling_recovery_tests.py', 'native_recovery_safety_tests.py', 'native_retirement_regression_tests.py',
    'native_integration_tests.py', 'startup_failure_tests.py', 'native_ui_tests.py', 'diy_package_page_tests.py',
    'diy_bundled_tests.py', 'diy_package_reload_tests.py', 'diy_reload_cache_tests.py', 'diy_medical_map_tests.py',
    'presence_compat_tests.py', 'condition_cleanup_tests.py', 'release_debug_tests.py', 'archive_guard_tests.py',
]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only', nargs='+', choices=CASES)
parser.add_argument('--keep-going', action='store_true', help='Run every requested check and report all failures.')
args = parser.parse_args()
selected = args.only
def source_hashes():
    return {path.relative_to(PROJECT/'src').as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((PROJECT/'src').rglob('*')) if path.is_file()}
def test_input_hashes():
    paths=list(TESTS.rglob('*.py'))+[PROJECT/'tools/local_candidate.py',PROJECT/'tools/release.py',PROJECT/'tools/archive_guard.py']
    return {path.relative_to(PROJECT).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}
source_before=source_hashes()
inputs_before=test_input_hashes()
failures = []
results = []
with (CHECKS/'tests.log').open('w',encoding='utf-8') as log:
    for case in selected or CASES:
        print(PROJECT.name + ': ' + case, flush=True)
        started = time.perf_counter()
        result=subprocess.run([sys.executable,str(TESTS/case)],cwd=PROJECT,
            text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=environment)
        log.write(case+'\n'+result.stdout+'\n'); log.flush()
        print(result.stdout, end='', flush=True)
        results.append(dict(case=case, exit_code=result.returncode, seconds=time.perf_counter()-started))
        if result.returncode:
            failures.append((case, result.returncode))
            if not args.keep_going: break
source_after=source_hashes()
inputs_after=test_input_hashes()
if source_before!=source_after or inputs_before!=inputs_after:
    failures.append(('source or test inputs changed during execution',1))
report = dict(selected=selected is not None, required=CASES, requested=selected or CASES, results=results,
              passed=len(results)==len(selected or CASES) and not failures,
              python=sys.version, executable=sys.executable,
              environment={key:os.environ.get(key) for key in ('DARKTIDE_SOURCE','DARKTIDE_TEST_RUNTIME','DARKTIDE_HED_SOURCE','DARKTIDE_SOLO_SOURCE')},
              source_before_sha256=source_before,source_after_sha256=source_after,
              test_inputs_before_sha256=inputs_before,test_inputs_after_sha256=inputs_after,
              source_payload_sha256=source_after)
(CHECKS/'tests-result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if failures:
    print(PROJECT.name + ': failed checks: ' + ', '.join(case for case, _ in failures), flush=True)
    sys.exit(1)
print(PROJECT.name + (': selected checks passed.' if selected else ': all project checks passed.'))
