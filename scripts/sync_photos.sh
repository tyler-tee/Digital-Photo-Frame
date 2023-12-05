#!/bin/bash

# Activate the virtual environment and sync our photos

source ~/Digital-Photo-Frame/venv/bin/activate
python ~/Digital-Photo-Frame/scripts/sync_photos.py
deactivate
