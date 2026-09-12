"""Real nested archives must fail, even with misleading filenames."""
import bz2, gzip, io, json, lzma, sys, tarfile, zipfile
from project_env import PROJECT, CHECKS
sys.path.insert(0, str(PROJECT / 'tools'))
from archive_guard import assert_no_nested_archives, nested_archive_type
from release import collect_sources

buffer=io.BytesIO()
with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('example.lua', 'return {}')
zip_bytes=buffer.getvalue()
buffer=io.BytesIO()
with tarfile.open(fileobj=buffer, mode='w') as archive:
    entry=tarfile.TarInfo('example.lua');data=b'return {}';entry.size=len(data)
    archive.addfile(entry,io.BytesIO(data))
tar_bytes=buffer.getvalue()
samples={
    'ZIP': zip_bytes, 'prefixed ZIP': b'MZ'+bytes(126)+zip_bytes,
    'gzip': gzip.compress(b'return {}'), 'bzip2': bz2.compress(b'return {}'),
    'xz': lzma.compress(b'return {}'), 'TAR': tar_bytes,
    '7z signature': b'7z\xbc\xaf\x27\x1c'+bytes(32),
    'RAR signature': b'Rar!\x1a\x07\x01\x00'+bytes(32),
    'CAB signature': b'MSCF'+bytes(32),
    'zstd signature': b'\x28\xb5\x2f\xfd'+bytes(32),
    'LZ4 signature': b'\x04\x22\x4d\x18'+bytes(32),
}
for kind,data in samples.items():
    assert nested_archive_type('looks_like_source.lua',data),kind
    try: assert_no_nested_archives({'looks_like_source.lua':data})
    except AssertionError as error: assert 'looks_like_source.lua' in str(error)
    else: raise AssertionError(kind)
assert nested_archive_type('asset.ZIP',b'not a valid archive')
assert_no_nested_archives({'source.lua':b'-- package.zip is an example name\nreturn {}',
                          'package.json':b'{"files":["lua/main.lua"]}'})
_,_,_,payloads=collect_sources()
assert_no_nested_archives(payloads)
original=PROJECT/'release/4.4.9/HavocConditionManager-4.4.9.zip'
with zipfile.ZipFile(original) as z:
    assert_no_nested_archives({entry.filename:z.read(entry) for entry in z.infolist()})
report=dict(renamed_archive_cases=len(samples),current_payload_files=len(payloads),
            original_449_nested_archives=0,nexus_server_verdict='unknown')
(CHECKS/'archive-guard-tests.json').write_text(json.dumps(report,indent=2))
print('Archive guard: ZIP/SFX, TAR, compressed streams and renamed files rejected; original 4.4.9 passes: PASS')
