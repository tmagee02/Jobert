from pathlib import Path
import json

folderNER = Path("./scraper/nlp/companyNER")
oldFile = Path("./scraper/nlp/companyNER/uberNER.json")

# data = json.loads(oldFile.read_text(encoding="utf-8"))
# print(data[0]['jobDesc'])

# Read the old JSON
with open(oldFile, "r", encoding="utf-8") as f:
    data = json.load(f)  # \uXXXX will automatically become the real character

# Write the new JSON with actual characters
with open(f'{folderNER}/uberNER_new.json', "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

