import spacy
from scraper.nlp.patternsNLP import patterns
import re
from typing import Tuple
from scraper.job import Job

def handleAllNLP(jobDetails: dict[str, Job]):
    nlp = spacy.load("./scraper/nlp/training/output/model-best")
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

    for job in jobDetails.values():
        text = f'{job.offices} ::: {job.remote}  <><><><>  {job.jobDesc}'
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

        try:
            minSalary, maxSalary = extractSalaryRange(labelLists['SALARY'][0]) if labelLists['SALARY'] else (-1, -1)
        except ValueError as e:
            print(f'ValueError Caught: {e}')
            minSalary, maxSalary = (-1, -1)

        try:
            minExp, maxExp = extractExperience(labelLists['EXPERIENCE'][0]) if labelLists['EXPERIENCE'] else (-1, -1)
        except ValueError as e:
            print(f'ValueError Caught: {e}')
            minExp, maxExp = (-1, -1)

        job.minSalary, job.maxSalary = minSalary, maxSalary
        job.minExperience, job.maxExperience = minExp, maxExp
        job.locations = labelLists['LOCATION']


def extractSalaryRange(salary: str) -> Tuple[int, int]:
    regex = r'\d{1,3}(?:,\d{3}){1,2}'
    salaryVals = re.findall(regex, salary)
    
    if len(salaryVals) != 1 and len(salaryVals) != 2:
        raise ValueError(f'Unexpected amount of values in salary string - {salary} >>> amount of values seen is {len(salaryVals)}')

    minSalary = int(salaryVals[0].replace(',', ''))
    maxSalary = int(salaryVals[1].replace(',', '')) if len(salaryVals) == 2 else minSalary

    return minSalary, maxSalary


def extractExperience(experience: str) -> Tuple[int, int]:
    regex = r'\d+'
    expVals = re.findall(regex, experience)
    
    if len(expVals) != 1 and len(expVals) != 2:
        raise ValueError(f'Unexpected amount of values in experience string - {experience}')

    minExp = int(expVals[0])
    maxExp = int(expVals[1]) if len(expVals) == 2 else minExp

    if minExp < 0 or minExp > 99 or maxExp < minExp or maxExp > 99:
        raise ValueError(f'Unwanted years of experience in experience string - {experience}')

    return minExp, maxExp




def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError
    return a / b