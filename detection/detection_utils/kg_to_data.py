import json
import csv

# transform a json knowledge graph to a tsv
def transform(kg, out):
    with open(kg) as kg_file:
        info = json.load(kg_file)
    data = []
    for key in info.keys():
        s = ""
        s += f"{info[key]['type']} name: {key}"
        if "description" in info[key].keys():
            s += f" {info[key]['type']} description: {info[key]['description']} "
        elif "events" in info[key].keys():
            s += f" {info[key]['type']} events: {', '.join(info[key]['events'])} "
        else:
            print(info[key].keys())
        data.append([s])
    with open(out, "w") as o:
        writer = csv.writer(o, delimiter = "\t")
        writer.writerows(data)

# change file paths as appropriate on your machine
transform("../../data/kg.json", "../../data/kg.tsv")
transform("../../data/kg2.json", "../../data/kg2.tsv")
