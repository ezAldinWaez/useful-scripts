"""
Shared Google Photos OAuth helper.
Keeps / refreshes credentials in token.pickle so all other scripts can `from auth import get_service`.
"""
from pathlib import Path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
TOKEN_FILE = Path(__file__).with_name("token.pickle")
CREDS_FILE = Path(__file__).with_name("credentials.json")


def _authenticate():
    creds = None
    if TOKEN_FILE.exists():
        creds = pickle.loads(TOKEN_FILE.read_bytes())

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_bytes(pickle.dumps(creds))
    return creds


def get_service():
    """Return an authorised Google Photos API client."""
    creds = _authenticate()
    return build("photoslibrary", "v1", credentials=creds, static_discovery=False)
