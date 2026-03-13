from typing import List, Tuple, Set
from collections import defaultdict
from scraper.utils import randomDelay
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
import logging
import time
from scraper.job import Job

def getLocator(page: Page, xpaths: dict, companyName: str, key: str) -> Locator:
        locDummy = page.locator('//h1/h1/h1/h1')
        xpath = xpaths[companyName][key]
        return page.locator(xpath) if xpath else locDummy


def getLocatorText(locator: Locator, onlyFirst: bool=False):
    if onlyFirst:
        return locator.nth(0).inner_text() if locator.count() > 0 else None
    else:
        return ' \n\n '.join(locator.all_inner_texts()) if locator.count() > 0 else None


def getJobDetails(page: Page, status: int, xpaths: dict, companyName: str, idCompany: int, jobDetails: dict, url: str) -> None:
    logger = logging.getLogger('Jobert Scraper')
    jobActivity = logging.getLogger('Job Activity')
    if status != 200:
        logger.error(f'Status {status} @ {url}. Skipping.')
        jobActivity.error(f'Status {status} @ {url}. Skipping.')
        return

    try:
        logger.info(f'Status {status} @ {url}. Good.')
        page.locator(xpaths[companyName]['jobTitle']).nth(0).wait_for(timeout=5000)
        locTitle = getLocator(page, xpaths, companyName, 'jobTitle')
        locJobDesc = getLocator(page, xpaths, companyName, 'jobDesc')
        locOffices = getLocator(page, xpaths, companyName, 'location')
        locRemote = getLocator(page, xpaths, companyName, 'remote')
        locDatePosted = getLocator(page, xpaths, companyName, 'datePosted')

        title = getLocatorText(locTitle, onlyFirst=True)
        jobDesc = getLocatorText(locJobDesc)
        offices = getLocatorText(locOffices)
        remote = getLocatorText(locRemote)
        datePosted = getLocatorText(locDatePosted)
        
        randomDelay(True)
        jobDetails[url] = Job(url, idCompany, title, jobDesc, offices, remote, datePosted)
        jobActivity.info(f'New job ( {title} ) found @ {url}')
        return 
    except PlaywrightTimeoutError:
        logger.error(f'Possible invalid job @ {url}.')
        jobActivity.error(f'Possible invalid job @ {url}.')
        return


def getAllJobDetails(dbJobUrls: Set[str], page: Page, jobUrls: List[Tuple[str, int, str]], xpaths: defaultdict) -> dict[str, Job]:   
    timeStart = time.perf_counter()
    logger = logging.getLogger('Jobert Scraper')
    jobActivity = logging.getLogger('Job Activity')
    jobDetails = {}
    count = 1
    companyCount = defaultdict(int)
    for company, idCompany, jobUrl in jobUrls:
        if jobUrl not in dbJobUrls and jobUrl not in jobDetails and companyCount[company] < 100:
            try:
                status = page.goto(jobUrl).status
                print(count, jobUrl)
                count += 1
                companyCount[company] += 1
                getJobDetails(page, status, xpaths, company, idCompany, jobDetails, jobUrl)
            except PlaywrightTimeoutError:
                logger.error(f'Possible invalid job @ {jobUrl}.')
                jobActivity.error(f'Possible invalid job @ {jobUrl}.')
        else:
            logger.info(f'Job details already gathered for {jobUrl}. Skipping.')

    timeEnd = time.perf_counter()
    timeGetAllJobDetails = timeEnd - timeStart
    print(f'\ngetAllJobDetails Time: {timeGetAllJobDetails}\n')
    return jobDetails