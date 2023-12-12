#!/bin/bash

# Activate the virtual environment and display our photos
source /home/pi/Digital-Photo-Frame/digital-photo-frame/bin/activate
python /home/pi/Digital-Photo-Frame/scripts/run_photo_display.py
deactivate