import re
import spacy
import logging
from typing import Tuple
from scraper.job import Job
from scraper.utils import timed
from scraper.nlp.patternsNLP import salaryPatterns, experiencePatterns

logger = logging.getLogger(__name__)

@timed('handleAllNLP', debugOnly=False)
def handleAllNLP(jobsScraped: list[Job]):
    nlp = spacy.load("./scraper/nlp/training/output/model-best")
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [*salaryPatterns, *experiencePatterns]
    ruler.add_patterns(patterns)

    for job in jobsScraped:
        text = f'{job.offices} ::: {job.remote}  <><><><>  {job.jobDesc}'
        doc = nlp(text)

        labelLists = {
            'SALARY' : [],
            'EXPERIENCE' : [],
            'LOCATION' : []
        }
        # labelLists = defaultdict(list)

        sentences = text.split("\n\n") #if job.title == 'Engineering Manager' else ''
        for sent in sentences:
            doc = nlp(sent)
            for ent in doc.ents:
                # labelLists[ent.label_].append(ent.text) you can use a defaultdict to test specific labels, changing them in patternsNLP
                if ent.label_ in labelLists:
                    # print(ent, ent.label_)
                    labelLists[ent.label_].append(ent.text)
                else:
                    print(f'possible issue: {ent.text} -> {ent.label_}')
        # print(labelLists['SALARY'], labelLists['EXPERIENCE'])

        try:
            minSalary, maxSalary = extractSalaryRange(labelLists['SALARY'][0]) if labelLists['SALARY'] else (None, None)
            job.minSalary, job.maxSalary = minSalary, maxSalary
        except ValueError as e:
            print(f'ValueError Caught: {e}\n')
            job.minSalary, job.maxSalary = None, None

        job.minExperience, job.maxExperience = extractExperience(job.url, labelLists['EXPERIENCE'])


def extractSalaryRange(salary: str) -> Tuple[int, int]:
    regexStandard = r'\d{1,3}(?:,?\d{3}){1,2}'
    regexK = r'\d{1,3}[kK]'
    salaryVals = re.findall(regexStandard, salary)
    salaryVals.extend(re.findall(regexK, salary))

    if len(salaryVals) != 1 and len(salaryVals) != 2:
        raise ValueError(f'Unexpected amount of values in salary string - {salary} >>> amount of values seen is {len(salaryVals)}')

    minString = salaryVals[0][:len(salaryVals[0])-1] if 'k' in salaryVals[0].lower() else salaryVals[0]
    maxString = salaryVals[1] if len(salaryVals) == 2 else salaryVals[0]
    maxString = maxString[:len(maxString)-1] if 'k' in maxString.lower() else maxString
    minSalary = int(minString.replace(',', ''))
    maxSalary = int(maxString.replace(',', ''))

    if 'k' in salaryVals[0].lower():
        minSalary *= 1000    
    if 'k' in salaryVals[0].lower():
        maxSalary *= 1000

    return minSalary, maxSalary


'''
Goes through each experience entity found and returns the first valid min/max YOE

Prints warnings of unexpected counts or YOE found in experience entities
'''
def extractExperience(jobUrl: str, experienceEntities: list[str]) -> Tuple[int | None, int | None]:            
    MAX_VALID_EXP = 20
    minExp, maxExp = None, None
    regex = r'\d+'
    
    for expEnt in experienceEntities:
        expVals = re.findall(regex, expEnt)
    
        if len(expVals) != 1 and len(expVals) != 2:
            logger.warning('%s - Unexpected amount of values in experience string - %s', jobUrl, expEnt)
            continue

        minExp = int(expVals[0])
        maxExp = int(expVals[1]) if len(expVals) == 2 else None

        if 0 <= minExp <= MAX_VALID_EXP and (maxExp is None or minExp < maxExp < 100):
            break
        else:
            logger.warning('%s - Unexpected years of experience in experience string - %s', jobUrl, expEnt)
            minExp, maxExp = None, None

    return minExp, maxExp