# Generates a latex table of the generated data in data.json
import json

def generate_row(data):
    proj_name = data['filename'][:-len(".zip")]
    obfuscation_methods_list = [
        ("$"+d[:1] + "_1$" if d == "Encode" else
         "$"+d[:1] + "_2$" if d == "Encrypt" else
         "-" if d == "" else
         d[:1])
        for d in data["obfuscation"]
    ]
    obfuscation_methods = " ".join(obfuscation_methods_list) if len(data["obfuscation"])>0 else "-"
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
    columns = ["", "ConstSub", "DeadCode", "Encode", "Encrypt", "VarSub", "DeadCode VarSub ConstSub Encode", "DeadCode VarSub ConstSub Encrypt Encode"]
    projs = {}
    for d in json_data:
        fn = d['filename']
        if not projs.get(fn):
            projs[fn] = []        
        projs[fn].append(d)
        
    
    rows = []
    for k, v in projs.items():
        row = [k[:-len(".zip")]] + ["-" for _ in range(len(columns))] # Row stats with project name
        for d in v:
            obfuscation_methods = " ".join([dd for dd in d["obfuscation"]])
            stats = d['data']['data']['attributes']['stats']
            detections = stats['malicious']
            undetected = stats['undetected']
            rate = "{:.2f}".format(detections/(undetected+detections))
            # Add in correct position
            if obfuscation_methods in columns:
                column_num = 1+columns.index(obfuscation_methods)
                row[column_num] = rate
        rows.append(row)
        print(" & ".join(row) + " \\\\")
    
    # CALCULATE AVG
    row = ["Average"] + ["0" for c in columns]
    for i, c in enumerate(columns):
        col_num = 1+i
        vals = []
        for r in rows:
            v = r[col_num]
            vals.append(float(v))
        avg_for_column = "{:.2f}".format(sum(vals) / len(vals)) if len(vals) > 0 else "-"
        row[col_num] = str(avg_for_column)
    print(" & ".join(row) + " \\\\")

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