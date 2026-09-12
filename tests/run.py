"""Run this project's checks; never build another release."""
from pathlib import Path
import os, subprocess, sys
TESTS=Path(__file__).resolve().parent
PROJECT=TESTS.parent
CHECKS=PROJECT/'build/checks'
CHECKS.mkdir(parents=True,exist_ok=True)
environment=dict(os.environ, PYTHONIOENCODING='utf-8')
with (CHECKS/'tests.log').open('w',encoding='utf-8') as log:
    for case in ['syntax_tests.py', 'diy_minion_lifecycle_tests.py', 'native_template_tests.py', 'native_intensity_profile_tests.py', 'native_elite_balance_tests.py', 'native_coordinated_load_tests.py', 'native_runtime_tests.py', 'native_pressure_tests.py', 'native_encounter_location_tests.py', 'native_reachable_placement_tests.py', 'native_door_placement_tests.py', 'native_special_pressure_tests.py', 'native_roamer_memory_tests.py', 'native_spawn_integrity_tests.py', 'native_spawn_smoothing_tests.py', 'native_straggler_tests.py', 'native_rear_ambient_tests.py', 'native_refill_optimization_tests.py', 'native_recycling_recovery_tests.py', 'native_recovery_safety_tests.py', 'native_retirement_regression_tests.py', 'native_integration_tests.py', 'startup_failure_tests.py', 'native_ui_tests.py', 'diy_package_page_tests.py', 'diy_package_reload_tests.py', 'diy_reload_cache_tests.py', 'diy_frenzied_assault_tests.py', 'native_melee_resource_tests.py', 'native_melee_installer_tests.py', 'diy_medical_map_tests.py', 'presence_compat_tests.py', 'condition_cleanup_tests.py', 'release_debug_tests.py']:
        print(PROJECT.name + ': ' + case, flush=True)
        result=subprocess.run([sys.executable,str(TESTS/case)],cwd=PROJECT,
            text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=environment)
        log.write(case+'\n'+result.stdout+'\n'); log.flush()
        print(result.stdout, end='', flush=True)
        if result.returncode: sys.exit(result.returncode)
print(PROJECT.name + ': all project checks passed.')
