#!/bin/bash

# Activate the virtual environment and sync our photos

source ~/Digital-Photo-Frame/digital-photo-frame/bin/activate
python ~/Digital-Photo-Frame/scripts/sync_photos.py
deactivate
