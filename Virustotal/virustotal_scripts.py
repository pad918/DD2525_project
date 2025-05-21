import dotenv
import requests
import json
from dotenv import load_dotenv, dotenv_values
import datetime
import os
load_dotenv()

url_upload = "https://www.virustotal.com/api/v3/files"
url_analysis = "https://www.virustotal.com/api/v3/analyses/"

def upload_file(file_path, meta_data):
    API_KEY = os.getenv("API_KEY")
    file_name = "decoder.exe"
    files = {"file": (file_name, open(file_path, "rb"), "application/x-msdownload")}
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    with open("data.json", "r+") as file:
        db = json.load(file)
    res = requests.post(url_upload, files=files, headers=headers)
    print(res.text)
    data = json.loads(res.text)
    analys_id = data["data"]["id"]

    new_upload = {
        "virustotal_id": analys_id,
        "name": "name",
        "filename": "filename",
        "obfuscation": "obfuscation",
        "type_of_malware": "type",
        "upload_date": "date",
        "data": []
    }

    db["uploads"].append(new_upload)
    with open('data.json', 'w') as f:
        json.dump(db, f, indent=4)

def update_database_uploads():
    API_KEY = os.getenv("API_KEY")
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    with open("data.json", "r+") as file:
        db = json.load(file)

    for upload in db["uploads"]:
        analys_id = upload["virustotal_id"]
        analysis_res = requests.get(url_analysis + analys_id, headers=headers)
        upload["data"].append(analysis_res.json())

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



get_ids()
print(get_stats_from_id("MzRjMWI1ODhhNDkwNTQ5NjA3OGEzOGJhOGFhZmU1MDM6MTc0NzgzNjA5Mg=="))
#upload_file("decoder.exe", {})
#update_database_uploads()




