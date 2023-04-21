import json
import csv

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

transform("/n/home04/khalevy/hate_speech_detection/data/post_level/kg.json", "/n/home04/khalevy/hate_speech_detection/data/post_level/kg.tsv")

transform("/n/home04/khalevy/hate_speech_detection/data/post_level/kg2.json", "/n/home04/khalevy/hate_speech_detection/data/post_level/kg2.tsv")
