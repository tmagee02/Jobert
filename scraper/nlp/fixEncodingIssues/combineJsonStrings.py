from pathlib import Path
import json

company = 'uber'
oldFile = Path(f"./scraper/nlp/companyNER/{company}NER.json")
newFile = Path(f"./scraper/nlp/companyNER/{company}NER_new.json")

try:
    oldData = json.loads(oldFile.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"Failed to parse {oldFile}: {e}")
    oldData = []

newData = []
for i, job in enumerate(oldData):
    updatedLocations = f'{job["locations"]}  <><><><>  '
    combined = updatedLocations + job['jobDesc']
    updatedEntities = []

    for start, end, entityType in job['entities']:
        if entityType == 'LOCATION':
            originalIndexes = [start, end, entityType]
            updatedEntities.append(originalIndexes)
        else:
            offset = len(updatedLocations)
            updatedIndexes = [start + offset, end + offset, entityType]
            updatedEntities.append(updatedIndexes)

    updatedJob = {
        'company': job['company'],
        'jobUrl': job['jobUrl'],
        'jobText': combined,
        'entities': updatedEntities
    }
    newData.append(updatedJob)

with open(newFile, "w", encoding="utf-8") as f:
    json.dump(newData, f, ensure_ascii=False, indent=4)