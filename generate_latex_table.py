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

def generate_comp_table(json_data):
    projs = {}
    for d in json_data:
        fn = d['filename']
        if not projs.get(fn):
            projs[fn] = []
        projs[fn].append(d)
    
    all_vals = []
    for k, v in projs.items():
        values = []
        values.append(k)
        for d in v:
            obfuscation_methods = " ".join([dd[:1] for dd in d["obfuscation"]])
            stats = d['data']['data']['attributes']['stats']
            detections = stats['malicious']
            undetected = stats['undetected']
            rate = "{:.2f}".format(detections/undetected)
            if(len(values)>=2):
                orig = float(values[1])
                new = detections/undetected
                #if (new>orig):
                #    rate = "\\textcolor{red}" + "{" + rate + "}"
            values.append(rate)
        all_vals.append([float(v) for v in values[1:]])

        print(" & ".join(values) + " \\\\")
    
    # CALCULATE AVG
    values = ["Avrage"]
    values.extend(["{:.2f}".format(sum([all_vals[j][i] for j in range(len(all_vals))])/len(all_vals)) for i in range(len(all_vals[0]))])
    print(" & ".join(values) + " \\\\")

def main():
    with open("data.json", "rt") as f:
        json_data = json.load(f)['uploads']

    generate_comp_table(json_data)

    print("-------------------")
        
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