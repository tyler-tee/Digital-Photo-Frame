#!/bin/bash

# Activate the virtual environment and sync our photos

source /home/pi/Digital-Photo-Frame/digital-photo-frame/bin/activate
python /home/pi/Digital-Photo-Frame/scripts/sync_photos.py
deactivate
