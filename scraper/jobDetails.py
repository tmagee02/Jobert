from typing import List, Tuple, Set
from collections import defaultdict
from utils import randomDelay
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
import logging

def getLocator(page: Page, xpaths: dict, companyName: str, key: str) -> Locator:
        locDummy = page.locator('//h1/h1/h1/h1')
        xpath = xpaths[companyName][key]
        return page.locator(xpath) if xpath else locDummy


def getLocatorText(locator: Locator, multiple: bool=False, onlyFirst: bool=False):
    if onlyFirst:
        return locator.nth(0).inner_text() if locator.count() > 0 else None
    elif multiple:
        return locator.all_inner_texts() if locator.count() > 0 else None
    else:
        return locator.inner_text() if locator.count() > 0 else None


def getJobDetails(page: Page, status: int, xpaths: dict, companyName: str, idCompany: int, jobDetails: dict, url: str) -> None:
    logger = logging.getLogger('Jobert Scraper')
    jobActivity = logging.getLogger('Job Activity')
    if status != 200:
        logger.error(f'Status {status} @ {url}. Skipping.')
        jobActivity.error(f'Status {status} @ {url}. Skipping.')
        return

    try:
        #might need to revert locTitle idk if it works
        page.locator(xpaths[companyName]['jobTitle']).nth(0).wait_for(timeout=5000)
        locTitle = getLocator(page, xpaths, companyName, 'jobTitle')
        locJobDesc = getLocator(page, xpaths, companyName, 'jobDesc')
        locLocations = getLocator(page, xpaths, companyName, 'location')
        locRemote = getLocator(page, xpaths, companyName, 'nextPage')
        locDatePosted = getLocator(page, xpaths, companyName, 'datePosted')

        # print(companyName, locTitle.count(), locJobDesc.count(), locLocations.count(), locRemote.count(), locDatePosted.count(), url)
        title = getLocatorText(locTitle, onlyFirst=True)
        jobDesc = getLocatorText(locJobDesc)
        locations = getLocatorText(locLocations, multiple=True)
        remote = getLocatorText(locRemote)
        datePosted = getLocatorText(locDatePosted)
        
        randomDelay(True)
        jobDetails[url] = (title, jobDesc, locations, remote, datePosted, idCompany)
        logger.info(f'Status {status} @ {url}. Good.')
        jobActivity.info(f'New job ( {title} ) found @ {url}')
        return 
    except PlaywrightTimeoutError:
        logger.error(f'Possible invalid job @ {url}.')
        jobActivity.error(f'Possible invalid job @ {url}.')
        return


def getAllJobDetails(dbJobUrls: Set[str], page: Page, jobUrls: List[Tuple[str, int, str]], xpaths: defaultdict) -> dict:   
    logger = logging.getLogger('Jobert Scraper')
    jobDetails = {}
    count = 1
    for company, idCompany, jobUrl in jobUrls:
        if jobUrl not in dbJobUrls and jobUrl not in jobDetails:
            status = page.goto(jobUrl).status
            print(count)
            count += 1
            getJobDetails(page, status, xpaths, company, idCompany, jobDetails, jobUrl)
        else:
            logger.info(f'Job details already gathered for {jobUrl}. Skipping.')
    return jobDetails