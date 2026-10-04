import json
import time
import urllib.request
import urllib.parse
import urllib.error
import sys
import os
from pathlib import Path
from .config import CREDENTIALS_FILE, TOKEN_FILE

SCOPES = "https://www.googleapis.com/auth/drive.file"

DEFAULT_CLIENT_ID = os.environ.get("AGY_GDRIVE_CLIENT_ID", "")
DEFAULT_CLIENT_SECRET = os.environ.get("AGY_GDRIVE_CLIENT_SECRET", "")

def load_credentials():
    if CREDENTIALS_FILE.exists():
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "client_id": DEFAULT_CLIENT_ID,
        "client_secret": DEFAULT_CLIENT_SECRET
    }

def save_credentials(client_id, client_secret):
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    creds = {"client_id": client_id, "client_secret": client_secret}
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f, indent=2)
    return creds

def load_tokens():
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_tokens(token_data):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)

def refresh_access_token(creds, refresh_token):
    url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            tokens = load_tokens() or {}
            tokens["access_token"] = res["access_token"]
            tokens["expires_at"] = time.time() + res.get("expires_in", 3600) - 60
            if "refresh_token" in res:
                tokens["refresh_token"] = res["refresh_token"]
            save_tokens(tokens)
            return tokens["access_token"]
    except urllib.error.HTTPError as e:
        print(f"Error refreshing access token: {e.read().decode('utf-8')}", file=sys.stderr)
        return None

def get_valid_access_token():
    tokens = load_tokens()
    if not tokens:
        print("No active Google Drive session. Please run 'agy-backup auth' first.", file=sys.stderr)
        return None
    
    creds = load_credentials()
    if time.time() >= tokens.get("expires_at", 0):
        refresh_tok = tokens.get("refresh_token")
        if refresh_tok and creds.get("client_id"):
            return refresh_access_token(creds, refresh_tok)
        else:
            print("Access token expired and no refresh token available. Run 'agy-backup auth'.", file=sys.stderr)
            return None
    return tokens.get("access_token")

def perform_device_flow_auth(client_id, client_secret):
    save_credentials(client_id, client_secret)
    
    # 1. Request device code
    url = "https://oauth2.googleapis.com/device/code"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "scope": SCOPES
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as resp:
            dev_res = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Failed to initiate device auth: {e.read().decode('utf-8')}", file=sys.stderr)
        return False

    verification_url = dev_res.get("verification_url", "https://www.google.com/device")
    user_code = dev_res["user_code"]
    device_code = dev_res["device_code"]
    interval = dev_res.get("interval", 5)
    expires_in = dev_res.get("expires_in", 1800)

    print("\n=======================================================")
    print("  GOOGLE DRIVE AUTHENTICATION")
    print("=======================================================")
    print(f"1. Open this URL in your browser:\n   \033[1;34m{verification_url}\033[0m")
    print(f"2. Enter this code when prompted: \033[1;32m{user_code}\033[0m")
    print("=======================================================\n")
    
    # Attempt termux-open-url if termux API available
    try:
        os.system(f"termux-open-url '{verification_url}' >/dev/null 2>&1")
    except Exception:
        pass

    print("Waiting for authorization (press Ctrl+C to cancel)...")
    
    token_url = "https://oauth2.googleapis.com/token"
    start_time = time.time()
    
    while time.time() - start_time < expires_in:
        time.sleep(interval)
        poll_data = urllib.parse.urlencode({
            "client_id": client_id,
            "client_secret": client_secret,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }).encode("utf-8")
        
        poll_req = urllib.request.Request(token_url, data=poll_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(poll_req) as resp:
                token_res = json.loads(resp.read().decode("utf-8"))
                tokens = {
                    "access_token": token_res["access_token"],
                    "refresh_token": token_res.get("refresh_token", ""),
                    "expires_at": time.time() + token_res.get("expires_in", 3600) - 60
                }
                save_tokens(tokens)
                print("\033[1;32m✓ Google Drive Authentication Successful!\033[0m")
                return True
        except urllib.error.HTTPError as e:
            err_body = json.loads(e.read().decode("utf-8"))
            err = err_body.get("error")
            if err == "authorization_pending":
                continue
            elif err == "slow_down":
                interval += 5
                continue
            elif err == "expired_token":
                print("Device code expired. Please re-run auth.", file=sys.stderr)
                return False
            else:
                print(f"Auth error: {err_body}", file=sys.stderr)
                return False

    print("Authentication timed out.", file=sys.stderr)
    return False
