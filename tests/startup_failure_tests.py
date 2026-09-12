"""Full entrypoint with the DMF failed-module return value."""
from pathlib import Path
import subprocess,sys
subprocess.run([sys.executable,str(Path(__file__).with_name('native_integration_tests.py')),'--failed-diy'],check=True)
