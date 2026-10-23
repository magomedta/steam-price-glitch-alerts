import os
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secrets.json")
TOKEN_PICKLE = os.path.join(os.path.dirname(__file__), "youtube_token.pickle")

def get_authenticated_service():
    """Authenticates with YouTube API and caches credentials."""
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"[!] Please place your YouTube OAuth client_secrets.json in {CLIENT_SECRETS_FILE}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PICKLE, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_short(video_path: str, title: str, description: str, tags: list):
    """Uploads a vertical video directly to YouTube Shorts."""
    youtube = get_authenticated_service()
    if not youtube:
        return False

    body = {
        "snippet": {
            "title": f"{title} #Shorts",
            "description": f"{description}\n\n⚡ Instant Alerts: https://t.me/price_glitch_live\n#Shorts #Steam #FreeGames #Gaming",
            "tags": tags + ["Shorts", "FreeGames", "Steam", "Gaming"],
            "categoryId": "20" # Gaming category
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"[*] Uploading {video_path} to YouTube Shorts...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Uploaded {int(status.progress() * 100)}%...")

    print(f"[✔] Upload Successful! Video ID: https://youtube.com/shorts/{response.get('id')}")
    return response.get("id")

if __name__ == "__main__":
    test_video = os.path.join(os.path.dirname(__file__), "shorts_output", "viral_promo_ad.mp4")
    if os.path.exists(test_video):
        print(f"Ready to upload: {test_video}")
        print("To enable 100% automated YouTube publishing, add client_secrets.json from Google Cloud Console.")
