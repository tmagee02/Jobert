from pathlib import Path
import json

oldFile = Path("./scraper/nlp/companyNER/uberNER.json")
newFile = Path("./scraper/nlp/companyNER/uberNER_new.json")

try:
    oldData = json.loads(oldFile.read_text())
except json.JSONDecodeError as e:
    print(f"Failed to parse {oldFile}: {e}")
    oldData = []

try:
    newData = json.loads(newFile.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"Failed to parse {newFile}: {e}")
    newData = []

j = 0
for old, new in zip(oldData, newData):
    print('\n', j, old['jobUrl'])
    oldJobDesc, oldLocations = old['jobDesc'], old['locations']
    newJobDesc, newLocations = new['jobDesc'], new['locations']

    for i in range(len(old['entities'])):
        oldStart, oldEnd, oldType = old['entities'][i]
        newStart, newEnd, newType = new['entities'][i]

        oldSlice = repr(oldLocations[oldStart : oldEnd]) if oldType == 'LOCATION' else repr(oldJobDesc[oldStart : oldEnd])
        newSlice = repr(newLocations[newStart : newEnd]) if newType == 'LOCATION' else repr(newJobDesc[newStart : newEnd])
        # print(oldStart, oldEnd, oldType, oldSlice, len(oldJobDesc))
        print(oldSlice, newSlice, oldType)
    j += 1