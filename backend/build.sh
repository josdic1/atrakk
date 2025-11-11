#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Run seed to populate database
python seed.py
