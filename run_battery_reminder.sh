#!/bin/bash
# Activate virtual environment
source /home/usama/crons/battery_reminder/venv/bin/activate

# Run Python script
/usr/bin/python3 /home/usama/crons/battery_reminder/main.py

deactivate