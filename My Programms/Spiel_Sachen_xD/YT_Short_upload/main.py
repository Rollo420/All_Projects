import json
import os
import requests

from google.oauth2 import service_account
from googleapiclient.discovery import build
from simple_youtube_api.youtube_api import SCOPE_YOUTUBE


def upload_short(file_path, title, description, tags):
    # Load the Client ID and Client Secret from the client_secret.json file.
    with open('client_secret.json', 'r') as f:
        data = json.load(f)
        data = data['installed']

    print(data)
    input()

    client_id = data['client_id']
    client_secret = data['client_secret']

    # Create OAuth2 credentials.
    credentials = service_account.Credentials.from_service_account_file(
        data['auth_provider_x509_cert_url'], scopes=SCOPE_YOUTUBE, client_id=client_id, client_secret=client_secret
    )

    client_id = data["client_id"]
    client_secret = data["client_secret"]

    # Create OAuth2 credentials.
    credentials = service_account.Credentials.from_service_account_file(
        data['auth_provider_x509_cert_url'], scopes=SCOPE_YOUTUBE, client_id=client_id, client_secret=client_secret
    )

    # Create a YouTube Data API service object.
    service = build("youtube", "v3", credentials=credentials)

    # Create a request to upload the short.
    request = service.videos().insert(
        part="snippet,status,contentDetails",
        media_body={"video": open(file_path, "rb")},
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
            },
            "status": {"privacyStatus": "public"},
            "contentDetails": {"duration": "PT60S"},
        },
    )

    # Make the request to the YouTube Data API.
    response = request.execute()

    return response

if __name__ == "__main__":
    file_path = "path/to/short.mp4"
    title = "This is a short."
    description = "This is a description of the short."
    tags = ["tag1", "tag2", "tag3"]

    # Upload the short to YouTube.
    response = upload_short(file_path, title, description, tags)

    # Check the response status code.
    if response.status_code == 200:
        print("Short successfully uploaded.")
        short_id = response["id"]
        print("Short ID:", short_id)
    else:
        print("Short upload failed.")
