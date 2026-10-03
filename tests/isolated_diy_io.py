"""Keep native DIY filesystem tests away from the user's saved packages."""
import atexit
import os
from pathlib import Path
from tempfile import TemporaryDirectory

_directory = None


def isolate():
    global _directory
    if _directory is not None:
        return Path(_directory.name)
    from project_env import CHECKS
    _directory = TemporaryDirectory(prefix='diy-test-', dir=CHECKS)
    root = Path(_directory.name)
    (root / 'Fatshark/Darktide').mkdir(parents=True)
    previous = os.environ.get('APPDATA')
    os.environ['APPDATA'] = str(root)

    def cleanup():
        if previous is None:
            os.environ.pop('APPDATA', None)
        else:
            os.environ['APPDATA'] = previous
        _directory.cleanup()

    atexit.register(cleanup)
    return root
