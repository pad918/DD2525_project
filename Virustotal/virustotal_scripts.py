import dotenv
import requests
import json
from dotenv import load_dotenv, dotenv_values
import datetime
import os
load_dotenv()

url_upload = "https://www.virustotal.com/api/v3/files"
url_analysis = "https://www.virustotal.com/api/v3/analyses/"
API_KEY = os.getenv("API_KEY")

def upload_file(file_path, meta_data):
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

    try:
        res = requests.post(url_upload, files=files, headers=headers)
        res.raise_for_status()
        data = json.loads(res.text)
        analys_id = data["data"]["id"]

        new_upload = {
            "virustotal_id": analys_id,
            "name": "name? of virus idk",
            "filename": file_name,
            "obfuscation": "obfuscation",
            "type_of_malware": "type",
            "upload_date": "date",
            "data": []
        }
        db["uploads"].append(new_upload)
        with open('data.json', 'w') as f:
            json.dump(db, f, indent=4)
        print(f"Uploaded {file_name} to virustotal")
    except Exception:
        exit(f"Error uploading file {file_name}, {res.text}")

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
        try:
            analysis_res = requests.get(url_analysis + analys_id, headers=headers)
            analysis_res.raise_for_status()
            upload["data"].append(analysis_res.json())
            print()
            if upload["data"][0]["data"]["attributes"]["status"] != "completed":
                print(f"{analys_id} not completed, try again later")
            else:
                print(f"File {analys_id} Updated")
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



#get_ids()
#print(get_stats_from_id("MzRjMWI1ODhhNDkwNTQ5NjA3OGEzOGJhOGFhZmU1MDM6MTc0NzgzNjA5Mg=="))
# upload_file("../Obfuscations/Encode.py", {})
# update_database_uploads()




