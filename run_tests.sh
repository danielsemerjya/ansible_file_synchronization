#!/usr/bin/env bash
set -e
if [ ! -d /tmp/virtualenv ]; then
    python3 -m venv /home/daniel/development/synchronize-file-4/tmp/virtualenv
fi
source /home/daniel/development/synchronize-file-4/tmp/virtualenv/bin/activate
pip --quiet install -r requirements.txt
python run_tests.py
deactivate