import spacy
from scraper.nlp.patternsNLP import patterns
import re
from typing import Tuple

def handleNLP(jobUrl, jobDesc, offices, remote):
    nlp = spacy.load("./scraper/nlp/training/output/model-best")
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    text = f'{offices} ::: {remote}  <><><><>  {jobDesc}'
    doc = nlp(text)

    labelLists = {
        'SALARY' : [],
        'EXPERIENCE' : [],
        'LOCATION' : []
    }

    sentences = text.split("\n\n")
    for sent in sentences:
        doc = nlp(sent)
        for ent in doc.ents:
            if ent.label_ in labelLists:
                labelLists[ent.label_].append(ent.text)
            else:
                print(f'possible issue: {ent.text} -> {ent.label_}')

    minSalary, maxSalary = extractSalaryRange(labelLists['SALARY'][0]) if labelLists['SALARY'] else (-1, -1)
    minExp, maxExp = extractExperience(labelLists['EXPERIENCE'][0]) if labelLists['EXPERIENCE'] else (-1, -1)
    
    print('\n', jobUrl)
    print(f'{minSalary}, {maxSalary} : SALARY')
    print(f'{minExp}, {maxExp} : EXPERIENCE')
    for location in labelLists['LOCATION']:
        print(f'{location} : LOCATION')


def extractSalaryRange(salary: str) -> Tuple[int, int]:
    regex = r'\d{1,3}(?:,\d{3}){1,2}'
    salaryVals = re.findall(regex, salary)
    
    if len(salaryVals) != 1 and len(salaryVals) != 2:
        print(-1, -1, salary, salaryVals)
        return (-1, -1)
        raise ValueError(f'Unexpected amount of values in salary string - {salary}')

    minSalary = int(salaryVals[0].replace(',', ''))
    maxSalary = int(salaryVals[1].replace(',', '')) if len(salaryVals) == 2 else minSalary

    # print(minSalary, maxSalary, salary, salaryVals)
    return minSalary, maxSalary


def extractExperience(experience: str) -> Tuple[int, int]:
    regex = r'\d+'
    expVals = re.findall(regex, experience)
    
    if len(expVals) != 1 and len(expVals) != 2:
        raise ValueError(f'Unexpected amount of values in experience string - {experience}')

    minExp = int(expVals[0])
    maxExp = int(expVals[1]) if len(expVals) == 2 else minExp

    if minExp > 99 or maxExp > 99:
        return (-1, -1)
        raise ValueError(f'Unwanted years of experience in experience string - {experience}')

    # print(minExp, maxExp, experience)
    return minExp, maxExp