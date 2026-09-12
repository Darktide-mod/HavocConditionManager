"""Reject nested archive payloads, including renamed files, before packaging."""
from pathlib import PurePosixPath
import io
import tarfile
import zipfile

ARCHIVE_SUFFIXES = {
    '.zip', '.7z', '.rar', '.tar', '.tgz', '.taz', '.tbz', '.tbz2', '.txz',
    '.gz', '.gzip', '.bz2', '.xz', '.lz', '.lzma', '.zst', '.zstd', '.lz4',
    '.cab', '.wim', '.swm', '.iso', '.jar', '.war', '.apk',
}
SIGNATURES = (
    (b'PK\x03\x04', 'ZIP'), (b'PK\x05\x06', 'ZIP'),
    (b'7z\xbc\xaf\x27\x1c', '7z'), (b'Rar!\x1a\x07', 'RAR'),
    (b'\x1f\x8b', 'gzip'), (b'BZh', 'bzip2'), (b'\xfd7zXZ\x00', 'xz'),
    (b'\x28\xb5\x2f\xfd', 'zstd'), (b'\x04\x22\x4d\x18', 'LZ4'),
    (b'LZIP', 'lzip'), (b'MSCF', 'CAB'), (b'MSWIM\x00\x00\x00', 'WIM'),
    (b'!<arch>\n', 'ar'), (b'xar!', 'xar'),
)


def nested_archive_type(name, data):
    suffix = PurePosixPath(name).suffix.lower()
    if suffix in ARCHIVE_SUFFIXES:
        return 'archive extension ' + suffix
    # ZIP central-directory detection also catches executable/SFX prefixes.
    if zipfile.is_zipfile(io.BytesIO(data)):
        return 'ZIP'
    for signature, kind in SIGNATURES:
        if data.startswith(signature):
            return kind
    # Inspect only an uncompressed TAR header; never inflate arbitrary streams.
    if len(data) >= 1024:
        try:
            with tarfile.open(fileobj=io.BytesIO(data), mode='r:'):
                return 'TAR'
        except (tarfile.TarError, OSError, ValueError):
            pass
    return None


def assert_no_nested_archives(payloads):
    for name, data in payloads.items():
        kind = nested_archive_type(name, data)
        if kind:
            raise AssertionError(f'Nested archive in release: {name} ({kind})')
