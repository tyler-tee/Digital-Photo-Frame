import json
import os
import requests
from requests_oauthlib import OAuth2Session


ABSOLUTE_PATH = os.path.dirname(__file__)
API_CONFIG = os.path.join(ABSOLUTE_PATH, "photos_api.json")
LOCAL_CONFIG = os.path.join(ABSOLUTE_PATH, "config.json")


def load_config():
    try:
        with open(API_CONFIG) as f:
            api_config = json.load(f)

        with open(LOCAL_CONFIG) as f:
            local_config = json.load(f)

        if api_config and local_config:
            return api_config, local_config

    except Exception as e:
        print(e)
        return None


def get_new_access_token():
    api_config, _ = load_config()

    extra = {
        'client_id': api_config['CLIENT_ID'],
        'client_secret': api_config['CLIENT_SECRET'],
    }

    google = OAuth2Session(api_config['CLIENT_ID'])
    new_token = google.refresh_token(api_config['TOKEN_URL'],
                                     refresh_token=api_config['REFRESH_TOKEN'],
                                     **extra)
    api_config['ACCESS_TOKEN'] = new_token['access_token']

    if 'refresh_token' in new_token.keys():
        api_config['REFRESH_TOKEN'] = new_token['refresh_token']

    with open(API_CONFIG, 'w') as f:
        f.write(json.dumps(api_config, indent=4))

    return new_token['access_token']


def get_photos():
    api_config, _ = load_config()

    headers = {
        "Authorization": f"Bearer {api_config['ACCESS_TOKEN']}"
    }

    payload = {
        "albumId": api_config['ALBUM_ID'],
        "pageSize": 100
    }

    response = requests.post('https://photoslibrary.googleapis.com/v1/mediaItems:search',
                             headers=headers, json=payload, timeout=10)

    if response.status_code == 200:
        items = response.json().get('mediaItems', [])
        return {item['filename']: item['baseUrl'] for item in items}

    else:
        new_token = get_new_access_token()

        headers['Authorization'] = f"Bearer {new_token}"

        response = requests.post('https://photoslibrary.googleapis.com/v1/mediaItems:search',
                                 headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            items = response.json().get('mediaItems', [])
            return {item['filename']: item['baseUrl'] for item in items}


def sync_photos():
    """
        Sync photos between Google Photos and a local folder.
    """
    _, local_config = load_config()
    local_folder = local_config['local_folder']

    # List photos in the Google Photos album
    photos = get_photos()

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
    sync_photos()
