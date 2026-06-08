from typing import List, Tuple, Set
from collections import defaultdict
from scraper.company import Company
from scraper.utils import randomDelay
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
import logging
import time
from scraper.job import Job

def getLocator(page: Page, company: Company, key: str) -> Locator:
        locDummy = page.locator('//h1/h1/h1/h1')
        xpath = company.xpaths[key]
        return page.locator(xpath) if xpath else locDummy


def getLocatorText(locator: Locator, onlyFirst: bool=False):
    if onlyFirst:
        return locator.nth(0).inner_text() if locator.count() > 0 else None
    else:
        return ' \n\n '.join(locator.all_inner_texts()) if locator.count() > 0 else None


def getJobDetails(page: Page, status: int, company: Company, jobDetails: dict, url: str) -> None:
    logger = logging.getLogger('Jobert Scraper')
    jobActivity = logging.getLogger('Job Activity')
    if status != 200:
        logger.error(f'Status {status} @ {url}. Skipping.')
        jobActivity.error(f'Status {status} @ {url}. Skipping.')
        return

    try:
        logger.info(f'Status {status} @ {url}. Good.')
        page.locator(company.xpaths['jobTitle']).nth(0).wait_for(timeout=5000)
        locTitle = getLocator(page, company, 'jobTitle')
        locOffices = getLocator(page, company, 'location')
        locRemote = getLocator(page, company, 'remote')
        locDatePosted = getLocator(page, company, 'datePosted')

        title = getLocatorText(locTitle, onlyFirst=True)
        jobDesc = getJobDesc(page, company)
        offices = getLocatorText(locOffices)
        remote = getLocatorText(locRemote)
        datePosted = getLocatorText(locDatePosted)
        
        randomDelay(True)
        jobDetails[url] = Job(url, company.id, title, jobDesc, offices, remote, datePosted)
        jobActivity.info(f'New job ( {title} ) found @ {url}')
        return 
    except PlaywrightTimeoutError:
        logger.error(f'Possible invalid job @ {url}.')
        jobActivity.error(f'Possible invalid job @ {url}.')
        return


def getAllJobDetails(page: Page, companies: defaultdict, jobUrls: List[Tuple[str, str]]) -> dict[str, Job]:  
    counts = defaultdict(int)
    for companyName, jobUrl in jobUrls:
        counts[companyName] += 1

    print(counts)
    MAX_COMPANY_COUNT = 5
    timeStart = time.perf_counter()
    logger = logging.getLogger('Jobert Scraper')
    jobActivity = logging.getLogger('Job Activity')
    jobDetails = {}
    count = 1
    companyCount = defaultdict(int)
    for companyName, jobUrl in jobUrls:
        if jobUrl not in jobDetails and companyCount[companyName] < MAX_COMPANY_COUNT:
            try:
                status = page.goto(jobUrl).status
                print(count, jobUrl)
                count += 1
                companyCount[companyName] += 1
                getJobDetails(page, status, companies[companyName], jobDetails, jobUrl)
            except PlaywrightTimeoutError:
                logger.error(f'Possible invalid job @ {jobUrl}.')
                jobActivity.error(f'Possible invalid job @ {jobUrl}.')
        else:
            logger.info(f'Job details already gathered for {jobUrl}. Skipping.')
    
    print('\nCompany URL Counts:')
    for company, count in companyCount.items():
        print(f'{company}: {count}')

    timeEnd = time.perf_counter()
    timeGetAllJobDetails = timeEnd - timeStart
    print(f'\ngetAllJobDetails Time: {timeGetAllJobDetails}\n')
    return jobDetails


def getJobDesc(page: Page, company: Company) -> str:
    sections = company.xpaths['jobDesc']
    sectionTexts = []

    try:
        for section in sections:
            sectionTexts.append(getLocatorText(page.locator(section), True))
    except PlaywrightTimeoutError:
        return 
    
    return '\n\n'.join(text for text in sectionTexts if text)