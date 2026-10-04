import time
import urllib.request
import urllib.parse
import json
import sys
import os
from pathlib import Path

CLIENT_ID = 'REDACTED'
CLIENT_SECRET = 'REDACTED'
DEVICE_CODE = "AH-1Ng1BDptHIf-jWJ7ky2tjif_OP7-QuDrgojdteTtMS3EFgtOlwBPYwNu064GcAQGlG64vIwzlGPS4z2s3oPAwzIu6nspeCg"
INTERVAL = 5
EXPIRES_IN = 1800

TOKEN_FILE = Path("/data/data/com.termux/files/home/.gemini/antigravity-cli/gdrive_token.json")
TOKEN_URL = "https://oauth2.googleapis.com/token"

start_time = time.time()
print("Polling Google OAuth token endpoint for device authorization...")

while time.time() - start_time < EXPIRES_IN:
    time.sleep(INTERVAL)
    poll_data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "device_code": DEVICE_CODE,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
    }).encode("utf-8")
    
    poll_req = urllib.request.Request(TOKEN_URL, data=poll_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(poll_req) as resp:
            token_res = json.loads(resp.read().decode("utf-8"))
            tokens = {
                "access_token": token_res["access_token"],
                "refresh_token": token_res.get("refresh_token", ""),
                "expires_at": time.time() + token_res.get("expires_in", 3600) - 60
            }
            TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_FILE, "w") as f:
                json.dump(tokens, f, indent=2)
            print("\033[1;32m✓ Google Drive Authentication Approved!\033[0m")
            
            # Execute cloud backup sync immediately!
            os.system("/data/data/com.termux/files/usr/bin/agy-backup backup")
            sys.exit(0)
    except urllib.error.HTTPError as e:
        err_body = json.loads(e.read().decode("utf-8"))
        err = err_body.get("error")
        if err == "authorization_pending":
            continue
        elif err == "slow_down":
            INTERVAL += 5
            continue
        elif err == "expired_token":
            print("Device code expired.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Auth error: {err_body}", file=sys.stderr)
            sys.exit(1)

print("Authentication timed out.", file=sys.stderr)
sys.exit(1)
