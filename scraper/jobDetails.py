from typing import List, Tuple, Set
from collections import defaultdict
from utils import randomDelay
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import logging


def getJobDetails(page: Page, status, xpaths: dict, companyName: str, idCompany: int, jobDetails: dict, url: str) -> None:
    #Uber has broken pages which i fixed and 7 h1s on a page
    #OpenAI has cloudflare captcha
    #Apple is consistant 11101
    #Databricks is consistant 11100
    logger = logging.getLogger('Jobert Scraper')
    if status != 200:
        logger.error(f'Status {status} @ {url}. Skipping.')
        return

    try:
        logger.info(f'Status {status} @ {url}. Good.')
        page.locator(xpaths[companyName]['jobTitle']).nth(0).wait_for(timeout=5000)
        locDummy = page.locator('//h1/h1/h1/h1')
        locTitle = page.locator(xpaths[companyName]['jobTitle']).nth(0) if xpaths[companyName]['jobTitle'] else locDummy
        locJobDesc = page.locator(xpaths[companyName]['jobDesc']) if xpaths[companyName]['jobDesc'] else locDummy
        locLocations = page.locator(xpaths[companyName]['location']) if xpaths[companyName]['location'] else locDummy
        locRemote = page.locator(xpaths[companyName]['nextPage']) if xpaths[companyName]['nextPage'] else locDummy
        locDatePosted = page.locator(xpaths[companyName]['datePosted']) if xpaths[companyName]['datePosted'] else page.locator('//h1/h1/h1/h1')

        # print(companyName, locTitle.count(), locJobDesc.count(), locLocations.count(), locRemote.count(), locDatePosted.count(), url)
        title = locTitle.inner_text() if locTitle.count() > 0 else None
        jobDesc = locJobDesc.inner_text() if locJobDesc.count() > 0 else None
        locations = locLocations.all_inner_texts() if locLocations.count() > 0 else None
        remote = locRemote.inner_text() if locRemote.count() > 0 else None
        datePosted = locDatePosted.inner_text() if locDatePosted.count() > 0 else None
        
        randomDelay(True)
        jobDetails[url] = (title, jobDesc, locations, remote, datePosted, idCompany)
        return 
    except PlaywrightTimeoutError:
        logger.error(f'Possible invalid job @ {url}.')
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