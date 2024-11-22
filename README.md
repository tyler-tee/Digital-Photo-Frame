# Digital Photo Frame

![SonarCloud Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=tyler-tee_Digital-Photo-Frame&metric=alert_status)


## Overview
Kivy-based application developed to run on a raspberry pi. Designed to display photos synced from a Google Photos album on a touchscreen display. Created for Christmas 2023 as a gift for my ~~fiance~~ wife and father.

## Key Features
- **Photo Synchronization**: Integrates with Google Photos API to sync photos.
- **Interactive UI**: Navigate through photos with touch gestures.
- **Weather and Time Display**: Fetches and shows current weather and time.
- **Automatic Updates**: Periodically syncs new photos and deletes old ones.

## Initial Setup
1. **Install Python**: Ensure Python >=3.9 is installed on your Raspberry Pi.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API and Local Settings**:
   - Create a `config.json` with keys like `api_service_name`, `api_version`, `scopes`, `local_folder`, and `album_id`.
   - Save your Google API credentials in `client_secret.json`.
     - [Get started w/ the Google API](https://developers.google.com/photos/library/guides/get-started)

## Running the Application
1. **Initial Photo Population**:
   - Run `sync_photos.py` initially to populate your local folder with photos from the specified Google Photos album.
   ```bash
   python sync_photos.py
   ```
2. **Start the Photo Display**:
   - After the initial setup, use `run_photo_display.py` to handle photo synchronization and display.
   ```bash
   python run_photo_display.py
   ```

## Notes
- The script uses the pickle module for saving and loading Google Photos client credentials.
- For new installations or invalid credentials, a login window will prompt you for authentication.

## Run as a Service
- A sample `.service` file is provided in `/services` for configuring the app to run with `systemctl`.

## License
This project is licensed under the MIT License.
