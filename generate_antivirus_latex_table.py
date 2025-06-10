import json

if __name__ == "__main__":
    anti_malware_dict = {}
    try:
        with open("data.json", "r") as file:
            db = json.load(file)
    except FileNotFoundError:
        exit("data.json was not found.")
    except:
        exit("error")
    # Add all possible AV to a dict
    if "uploads" in db and db["uploads"]:
        first_upload_results = db["uploads"][0]["data"]["data"]["attributes"]["results"]
        for av_name in first_upload_results:
            anti_malware_dict[av_name] = {"hits": 0, "scans": 0}

    for upload in db["uploads"]:
        results = upload["data"]["data"]["attributes"]["results"]

        for name, result_data in results.items():
            if name in anti_malware_dict:
                if not result_data["category"] in ["type-unsupported"]:
                    anti_malware_dict[name]["scans"] += 1
                    # If its detected
                    if result_data["category"] in ["malicious", "suspicious"]:
                        anti_malware_dict[name]["hits"] += 1
    sorted_dict = dict(sorted(anti_malware_dict.items(), key=lambda item: item[1]['hits'], reverse=True))
    # Latex table gen
    for name, data in sorted_dict.items():
        hits = data['hits']
        scans = data['scans']
        if (hits or scans) > 0:
            print(f"{name} & {hits} & {scans}  & {round(hits / scans, 2)} \\\\")
