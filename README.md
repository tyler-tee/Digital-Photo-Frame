# Digital Photo Frame

## Overview
Python and Kivy-based application (intended to run on a raspberry pi), designed to display photos from a Google Photos album on a touchscreen display. Created for Christmas 2023 as a gift for my fiance and father.

## Key Features
- **Photo Synchronization**: Syncs with Google Photos to display images.
- **Interactive Touchscreen UI**: Navigate photos with touch gestures.
- **Weather and Time Display**: Shows real-time weather updates and time.
- **Automatic Updates**: Periodically syncs new photos and deletes old ones.

## Setup and Installation
1. **Install Python**: Ensure Python is installed on your Raspberry Pi.
2. **Install Dependencies**: Run `pip install -r requirements.txt` to install required packages.
3. **Configuration Files**: Set up `config.json` for local settings and `client_secret.json` for Google API access.
    - [Get started w/ the Google API](https://developers.google.com/photos/library/guides/get-started)
5. **Initial Photo Sync**: Execute `python sync_photos.py` for initial population of photos.
6. **Run the Photo Display**: Use `python run_photo_display.py` to start the primary application.

## Usage
- After the initial setup, `run_photo_display.py` manages photo synchronization and display.
- Users can interact with the touchscreen to navigate through their photos.

## Run as a Service
- A sample `.service` file is provided in `/services` for configuring the app to run with `systemctl`.

## License
This project is licensed under the MIT License.