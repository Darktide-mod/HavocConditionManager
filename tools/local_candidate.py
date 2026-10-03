"""Build/check a local test candidate; never uses the public-release pipeline."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import sys
import zipfile

from archive_guard import assert_no_nested_archives
from release import PACKAGE_EXTENSIONS

ROOT = Path(__file__).resolve().parents[1]
MOD = 'HavocConditionManager'
SOURCE = ROOT / 'src' / MOD


def payload():
    files = {}
    for path in sorted(SOURCE.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT / 'src').as_posix()
        assert path.suffix.lower() in PACKAGE_EXTENSIONS or (
            path.suffix.lower() == '.png' and 'docs/diy/package-examples/' in relative and '/resources/' in relative), relative
        assert '/native-melee/' not in relative and 'frenzied_assault' not in relative, relative
        data = path.read_bytes()
        assert not data.startswith((b'MZ', b'\x7fELF')), relative
        files[relative] = data
    for path in (f'{MOD}/{MOD}.mod', f'{MOD}/info.json', f'{MOD}/CHANGELOG.md',
                 f'{MOD}/scripts/mods/{MOD}/{MOD}.lua'):
        assert path in files, path
    assert_no_nested_archives(files)
    return files


def suite_evidence(files):
    evidence_path = ROOT / 'build/checks/tests-result.json'
    evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
    assert evidence['passed'] and not evidence['selected'], 'Run the complete tests/run.py aggregate before packaging.'
    assert evidence['source_payload_sha256'] == {name:hashlib.sha256(data).hexdigest() for name,data in files.items()}, 'Suite evidence must match the packaged source bytes.'
    return evidence_path, evidence


def validate(archive, files, version):
    evidence_path, evidence = suite_evidence(files)
    runtime = os.environ.get('DARKTIDE_TEST_RUNTIME')
    assert runtime, 'Set DARKTIDE_TEST_RUNTIME to the already approved isolated runtime.'
    sys.path.insert(0, runtime)
    from lupa.luajit21 import LuaRuntime
    lua = LuaRuntime(unpack_returned_tuples=True)
    compile_lua = lua.eval('function(s,n) local f,e=loadstring(s,n);return f~=nil,e end')
    count = 0
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(files) and set(names) == set(files)
        assert len({name.casefold() for name in names}) == len(names)
        for entry in z.infolist():
            path = PurePosixPath(entry.filename)
            assert path.parts[0] == MOD and '..' not in path.parts and not path.is_absolute()
            assert not entry.flag_bits & 1 and entry.compress_type == zipfile.ZIP_DEFLATED
            data = z.read(entry)
            assert data == files[entry.filename], entry.filename
            if path.suffix in ('.lua', '.mod'):
                text = data.decode('utf-8-sig')
                ok, error = compile_lua(text, entry.filename)
                assert ok, (entry.filename, error)
                count += 1
                for target in re.findall(r'io_dofile\(\s*"([^"]+)"', text):
                    if target.split('/')[0] == MOD:
                        assert target + '.lua' in files, (entry.filename, target)
        assert json.loads(z.read(f'{MOD}/info.json'))['version'] == version
    return {'kind': 'local test candidate; not a public release', 'version': version,
            'archive': str(archive), 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
            'archive_bytes': archive.stat().st_size, 'entries': len(files), 'compiled_lua_mod_files': count,
            'crc_layout_payload_import_checks': 'passed', 'nested_archives': 0,
            'full_suite': f"passed: {len(evidence['results'])} complete offline regression scripts",
            'suite_evidence': str(evidence_path),
            'suite_evidence_sha256': hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
            'live_gameplay': 'not performed', 'fps_claim': False,
            'payload_sha256': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
files = payload()
version = json.loads(files[f'{MOD}/info.json'])['version']
assert re.fullmatch(r'\d+\.\d+\.\d+-test\.\d+', version), 'Local candidates use the existing test-version convention.'
directory = ROOT / 'build/local-candidates' / version
directory.mkdir(parents=True, exist_ok=True)
assert directory.resolve().is_relative_to((ROOT / 'build').resolve())
archive = directory / f'{MOD}-{version}.zip'
if not args.check:
    assert not archive.exists(), 'Existing candidates are immutable; use --check or a new test version.'
    suite_evidence(files)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in files.items():
            entry = zipfile.ZipInfo(name, date_time=(2026, 10, 3, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, data)
report = validate(archive, files, version)
(directory / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({key: value for key, value in report.items() if key != 'payload_sha256'}, indent=2))
