import json
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.errors
import requests


def load_config():
    # Get the path to our config file
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(config_path) as config_file:
        config = json.load(config_file)

    client_secrets = os.path.join(os.path.dirname(__file__), 'client_secret.json')

    return config, client_secrets


# Load configuration
config, client_secrets = load_config()


def auth_client():
    """
    Authenticate our Google Photos client

    Returns:
        Service instance generated by the Google API
    """

    # Check if we already have saved credentials
    credentials = None
    pickle_path = os.path.join(os.path.dirname(__file__), 'token.pickle')
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets, config['scopes'])
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(pickle_path, 'wb') as token:
            pickle.dump(credentials, token)

    service = googleapiclient.discovery.build(
        config['api_service_name'], config['api_version'], credentials=credentials)

    return service


def list_photos(service, album_id: str) -> dict:
    """
       Summary: List photos in our Google Photos album

    Args:
        service: Service generated by the Google API
        album_id (str): ID of the album from which we want to list photos

    Returns:
        Dictionary of photo filenames and their URLs
    """
    results = service.mediaItems().search(body={"albumId": album_id}).execute()
    items = results.get('mediaItems', [])
    return {item['filename']: item['baseUrl'] for item in items}


def sync_photos(local_folder: str, album_id: str):
    """
        Sync photos between Google Photos and a local folder.

    Args:
        local_folder (str): Location of our local photos folder.
        album_id (str): ID of the album from which we want to download photos
    """

    service = auth_client()
    # List photos in the Google Photos album
    photos = list_photos(service, album_id)

    # Check if no photos are returned from Google Photos
    if not photos:
        print("No photos returned from Google Photos. Local folder remains unchanged.")
        return  # Skip updating the local folder if no photos are found

    photos_path = os.path.join(os.path.dirname(__file__), local_folder)
    # Download new photos
    for filename, url in photos.items():
        local_path = os.path.join(photos_path, filename)
        if not os.path.exists(local_path):
            response = requests.get(url)
            if response.status_code == 200:
                with open(local_path, 'wb') as file:
                    file.write(response.content)

    # Delete photos not in the album
    for filename in os.listdir(photos_path):
        if filename not in photos:
            os.remove(os.path.join(photos_path, filename))


if __name__ == '__main__':
    sync_photos(config['local_folder'], config['album_id'])
