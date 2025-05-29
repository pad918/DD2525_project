# Generates a latex table of the generated data in data.json
import json

def generate_row(data):
    proj_name = data['filename'][:-len(".zip")]
    obfuscation_methods = " ".join([d[:1] for d in data["obfuscation"]])

    status = data['data']['data']['attributes']['status']
    if(status != "completed"):
        return None
    stats = data['data']['data']['attributes']['stats']
    detections = stats['malicious']
    undetected = stats['undetected']
    scans = detections+undetected
    facts = [proj_name, obfuscation_methods, str(detections), str(scans), "{:.2f}".format(detections/scans)]
    return f"{' & '.join(facts)} \\\\"

def main():
    with open("data.json", "rt") as f:
        json_data = json.load(f)['uploads']

    for d in json_data:
        try:
            row = generate_row(d)
        except BaseException as e:
            row = "ERROR \\\\"
            raise e
        if(row):
            print(row)
    
if __name__ == "__main__":
    main()