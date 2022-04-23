#!/usr/bin/env bash
set -e
if [ ! -d /tmp/virtualenv ]; then
    python3 -m venv /tmp/virtualenv
fi
source /tmp/virtualenv/bin/activate
pip --quiet install -r requirements.txt
python run_tests.py
deactivate