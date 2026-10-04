import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from .auth import get_valid_access_token
from .config import GDRIVE_FOLDER_NAME

DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"
UPLOAD_API_BASE = "https://www.googleapis.com/upload/drive/v3"

def _make_request(url, method="GET", headers=None, data=None):
    token = get_valid_access_token()
    if not token:
        raise RuntimeError("Not authenticated with Google Drive.")

    req_headers = {
        "Authorization": f"Bearer {token}"
    }
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read()
            if "application/json" in content_type:
                return json.loads(body.decode("utf-8"))
            return body
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"Google Drive API error ({e.code}): {err_msg}")

def get_or_create_backup_folder():
    query = f"name = '{GDRIVE_FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    params = urllib.parse.urlencode({"q": query})
    url = f"{DRIVE_API_BASE}/files?{params}"
    
    res = _make_request(url)
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    
    # Create folder
    create_url = f"{DRIVE_API_BASE}/files"
    data = json.dumps({
        "name": GDRIVE_FOLDER_NAME,
        "mimeType": "application/vnd.google-apps.folder"
    }).encode("utf-8")
    
    folder_res = _make_request(create_url, method="POST", headers={"Content-Type": "application/json"}, data=data)
    return folder_res["id"]

def find_remote_file_by_name(filename, folder_id):
    query = f"name = '{filename}' and '{folder_id}' in parents and trashed = false"
    params = urllib.parse.urlencode({"q": query, "fields": "files(id, name, createdTime)"})
    url = f"{DRIVE_API_BASE}/files?{params}"
    res = _make_request(url)
    files = res.get("files", [])
    return files[0] if files else None

def upload_or_update_file(file_path, folder_id, description=""):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = file_path.name
    content_type = "application/gzip" if filename.endswith(".tar.gz") else "text/plain"

    existing_file = find_remote_file_by_name(filename, folder_id)

    boundary = "----AGYBackupBoundary7MA4YWxkTrZu0gW"
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    body_parts = []
    
    if existing_file:
        file_id = existing_file["id"]
        metadata = {"description": description}
        upload_url = f"{UPLOAD_API_BASE}/files/{file_id}?uploadType=multipart"
        method = "PATCH"
        action_name = "Updated"
    else:
        metadata = {"name": filename, "parents": [folder_id], "description": description}
        upload_url = f"{UPLOAD_API_BASE}/files?uploadType=multipart"
        method = "POST"
        action_name = "Uploaded"

    body_parts.append(f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(metadata)}\r\n".encode("utf-8"))
    body_parts.append(f"--{boundary}\r\nContent-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body_parts.append(file_bytes)
    body_parts.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    full_body = b"".join(body_parts)

    headers = {
        "Content-Type": f"multipart/related; boundary={boundary}",
        "Content-Length": str(len(full_body))
    }

    res = _make_request(upload_url, method=method, headers=headers, data=full_body)
    res["_action"] = action_name
    return res

def list_backups(folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    params = urllib.parse.urlencode({
        "q": query,
        "fields": "files(id,name,size,createdTime,description)",
        "orderBy": "createdTime desc"
    })
    url = f"{DRIVE_API_BASE}/files?{params}"
    
    res = _make_request(url)
    return res.get("files", [])

def download_file(file_id, target_path):
    url = f"{DRIVE_API_BASE}/files/{file_id}?alt=media"
    content = _make_request(url)
    
    target_path = Path(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target_path, "wb") as f:
        if isinstance(content, str):
            f.write(content.encode("utf-8"))
        else:
            f.write(content)
    return target_path

def delete_file(file_id):
    url = f"{DRIVE_API_BASE}/files/{file_id}"
    _make_request(url, method="DELETE")
