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
        locTitle = page.locator(xpaths[companyName]['jobTitle']).nth(0) if xpaths[companyName]['jobTitle'] else page.locator('//h1/h1/h1/h1')
        locJobDesc = page.locator(xpaths[companyName]['jobDesc']) if xpaths[companyName]['jobDesc'] else page.locator('//h1/h1/h1/h1')
        locLocations = page.locator(xpaths[companyName]['location']) if xpaths[companyName]['location'] else page.locator('//h1/h1/h1/h1')
        locRemote = page.locator(xpaths[companyName]['nextPage']) if xpaths[companyName]['nextPage'] else page.locator('//h1/h1/h1/h1')
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
    
