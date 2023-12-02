# Digital Photo Frame
This project is designed to populate photos displayed on digital picture frames powered by Raspberry Pi's for Christmas 2023. The script `sync_photos.py` is used to synchronize photos between Google Photos and a local folder.

# How it works
The script uses the Google Photos API to authenticate a client, list photos in a specified Google Photos album, and sync those photos with a local folder. It also deletes any photos in the local folder that are not in the Google Photos album.

# Setup
You need to have Python installed on your machine.
Install the required Python packages with pip install -r requirements.txt.
You need to have a config.json file in the same directory as the script. This file should contain the following keys:
api_service_name: The name of the Google API service.
api_version: The version of the Google API service.
scopes: The scopes for the Google API service.
local_folder: The path to the local folder where photos will be synced.
album_id: The ID of the Google Photos album.
You also need to have a client_secret.json file in the same directory as the script. This file should contain your Google API client secrets.
# Usage
Run the script with `python sync_photos.py`. The script will authenticate the Google Photos client, list the photos in the specified Google Photos album, download new photos to the local folder, and delete any photos in the local folder that are not in the Google Photos album.

# Note
The script uses the pickle module to save and load credentials for the Google Photos client. If no valid credentials are found, the script will open a new window for the user to log in. The credentials will be saved in a file named token.pickle in the same directory as the script.

# License
MIT