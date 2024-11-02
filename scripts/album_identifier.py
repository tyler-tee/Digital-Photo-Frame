import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def authenticate():
    # Authenticate using the client_secret.json file
    client_secrets = os.path.join(os.path.dirname(__file__), 'client_secret.json')
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
    creds = flow.run_local_server(port=0)
    return build("photoslibrary", "v1", credentials=creds)


def list_albums(service):
    # Retrieve albums from Google Photos
    results = service.albums().list(pageSize=50).execute()
    albums = results.get('albums', [])

    if not albums:
        print("No albums found.")
        return []

    # Display albums
    print("\nAlbums found:")
    for idx, album in enumerate(albums, start=1):
        print(f"{idx}. {album['title']}")

    return albums


def update_config(album_id):
    # Path to config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        # Load existing config.json data
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)

        # Update album_id
        config_data['album_id'] = album_id

        # Write updated data back to config.json
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        print("Album ID successfully updated in config.json.")

    except FileNotFoundError:
        print("config.json file not found.")
    except json.JSONDecodeError:
        print("Error reading config.json.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Authenticate and initialize the Google Photos service
    service = authenticate()
    if not service:
        return

    # List albums and prompt the user to select one
    albums = list_albums(service)
    if not albums:
        return

    try:
        choice = int(input("\nEnter the number of the album to retrieve its ID: ")) - 1
        if 0 <= choice < len(albums):
            album_id = albums[choice]['id']
            print(f"\nThe ID for the album '{albums[choice]['title']}' is: {album_id}")

            # Ask user if they want to save the album ID in config.json
            save_choice = input("Do you want to save this album ID to config.json? (yes to confirm): ").strip().lower()
            if save_choice in ['yes', 'y']:
                update_config(album_id)
            else:
                print("Album ID not saved.")
        else:
            print("Invalid choice.")

    except ValueError:
        print("Please enter a valid number.")


if __name__ == '__main__':
    main()
