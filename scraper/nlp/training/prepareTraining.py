import spacy
from spacy.tokens import DocBin
from pathlib import Path
import json
import math


def main():
    trainingFolder = Path('./scraper/nlp/training')
    
    trainingData = getData(purpose='training')
    docBinTraining = createDocBin(trainingData)
    docBinTraining.to_disk(f"./{trainingFolder}/train.spacy")

    devData = getData(purpose='dev')
    docBinDev = createDocBin(devData)
    docBinDev.to_disk(f"./{trainingFolder}/dev.spacy")

    testingData = getData(purpose='testing')
    docBinTesting = createDocBin(testingData)
    docBinTesting.to_disk(f"./{trainingFolder}/test.spacy")


def getData(purpose):
    folder = Path("./scraper/nlp/companyNER")
    config = Path("./scraper/nlp/config.json")
    testSet = set(json.loads(config.read_text())['testFiles'])

    files = []
    for file in folder.glob('*.json'):
        if purpose == 'testing' and file.name in testSet:
            files.append(file)
        elif purpose != 'testing' and file.name not in testSet:
            files.append(file)

    data = []
    for file in files:
        #get list of json objects (jobs)
        try:
            jobs = json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Failed to parse {file}: {e}")
            jobs = []

        #get wanted range of jobs for data
        if purpose == 'training':
            iStart, iEnd = 0, math.floor(len(jobs) * .8)
        elif purpose == 'dev':
            iStart, iEnd = math.floor(len(jobs) * .8), len(jobs)
        elif purpose == 'testing':
            iStart, iEnd = 0, len(jobs)

        
        for i in range(iStart, iEnd):
            job = jobs[i]

            jobText = job['jobText']
            entities = job['entities']
            data.append((jobText, entities))
    return data


def createDocBin(trainingData) -> DocBin:
    nlp = spacy.blank('en')
    docbin = DocBin()
    for text, entities in trainingData:
        doc = nlp(text)
        ents = []
        for start, end, entityType in entities:
            span = doc.char_span(start, end, label=entityType)
            if span is None:
                print(f"Skipping entity {entityType} at ({start}, {end})", repr(text[start:end]))
            else:
                ents.append(span)
        doc.ents = ents
        docbin.add(doc)
    return docbin


if __name__ == '__main__':
    main()