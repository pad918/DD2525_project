import dotenv
import requests
import json
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import hashlib
import os

load_dotenv()

url_upload = "https://www.virustotal.com/api/v3/files"
url_analysis = "https://www.virustotal.com/api/v3/analyses/"
url_large_file = "https://www.virustotal.com/api/v3/files/upload_url"
API_KEY = os.getenv("API_KEY")


def upload_file(file_path, obfuscations):
    file_size = os.path.getsize(file_path)
    url = url_upload
    hash_file = ""

    file_name = os.path.basename(file_path)
    files = {"file": (file_name, open(file_path, "rb"), "application/x-msdownload")}
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump({"uploads": []}, f, indent=4)
    with open("data.json", "r") as file:
        db = json.load(file)

    # If size larger than 32mb, upload to differnt url
    if file_size >= 32000000:
        try:
            upload_url_data = requests.get(url_large_file, headers=headers)
            upload_url_data.raise_for_status()
            data = json.loads(upload_url_data.text)
            url = data["data"]

        except Exception as e:
            exit(f"Error uploading file {file_name}, {upload_url_data.text}, {e}")
    # Compute the hash of file
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            hash_file = sha256_hash.hexdigest()

    except Exception as e:
        exit(e)

    try:
        res = requests.post(url, files=files, headers=headers)
        res.raise_for_status()
        data = json.loads(res.text)
        analys_id = data["data"]["id"]
        encoded_file_path = file_path.encode('utf-8')

        new_upload = {
            "virustotal_id": analys_id,
            "filename": file_name,
            "path": file_path,
            "size_bytes": file_size,
            "sha-256 hash": hash_file,
            "obfuscation": obfuscations,
            "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": []
        }
        db["uploads"].append(new_upload)
        with open('data.json', 'w') as f:
            json.dump(db, f, indent=4)
        print(f"Uploaded {file_name} to virustotal", f"url: https://www.virustotal.com/gui/file/{hash_file}")
    except Exception as e:
        exit(f"Error uploading file {file_name}, {res.text}, {e}")


def update_database_uploads():
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    if not os.path.exists("data.json"):
        exit("No item to update, upload an item first")
    with open("data.json", "r+") as file:
        db = json.load(file)

    for upload in db["uploads"]:
        analys_id = upload["virustotal_id"]
        filename = upload["filename"]
        try:
            analysis_res = requests.get(url_analysis + analys_id, headers=headers)
            analysis_res.raise_for_status()
            upload["data"].append(analysis_res.json())
            print()
            if upload["data"][0]["data"]["attributes"]["status"] != "completed":
                print(f"{analys_id} not completed, try again later")
            else:
                print(f"File {filename}, {analys_id} Updated")
        except Exception as e:
            exit(f"Error getting status for {analys_id} {e}")

    with open('data.json', 'w') as f:
        json.dump(db, f, indent=4)


def get_stats_from_id(id):
    with open("data.json", "r+") as file:
        db = json.load(file)
        for upload in db["uploads"]:
            if upload["virustotal_id"] == id:
                return upload["data"][0]["data"]["attributes"]["stats"]
    return None


def get_ids():
    with open("data.json", "r+") as file:
        db = json.load(file)
    for upload in db["uploads"]:
        print(upload["virustotal_id"])


# get_ids()
# print(get_stats_from_id("MzRjMWI1ODhhNDkwNTQ5NjA3OGEzOGJhOGFhZmU1MDM6MTc0NzgzNjA5Mg=="))
#upload_file("../Obfuscations/VarSub.py", ["Encryption", "test"])
#update_database_uploads()
