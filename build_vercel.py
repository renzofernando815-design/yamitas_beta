import os
import subprocess
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
TARGET_DIR = os.path.join(ROOT_DIR, '.vercel_python_packages')
REQUIREMENTS_FILE = os.path.join(ROOT_DIR, 'requirements.txt')

os.makedirs(TARGET_DIR, exist_ok=True)

print('Installing Python dependencies to', TARGET_DIR)
subprocess.check_call([
    sys.executable,
    '-m',
    'pip',
    'install',
    '--upgrade',
    '--target',
    TARGET_DIR,
    '-r',
    REQUIREMENTS_FILE,
])

sys.path.insert(0, TARGET_DIR)

import build_static

build_static.main()
