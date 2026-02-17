from pathlib import Path
import json

folder = Path("./scraper/nlp/companyNER")

toFile = []
for file in folder.glob('*.json'):
    #get list of json objects
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Failed to parse {file}: {e}")
        data = []

    for i, dic in enumerate(data):
        print('\n', i, dic['jobUrl'])
        toFile.append("")
        toFile.append(f"{i}, {dic['jobUrl']}")
        text = dic['jobText']

        for start, end, entityType in dic['entities']:
            entity = text[start : end]

            print(repr(entity))
            toFile.append(f"{repr(entity)},")


with open(f"{folder}/viewCompanyNERs.txt", "w", encoding="utf-8") as f:
    for line in toFile:
        f.write(f"{line}\n")