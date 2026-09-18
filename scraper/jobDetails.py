import asyncio
from asyncio import Semaphore
from playwright.async_api import Browser
from typing import List, Tuple
from collections import defaultdict
from scraper.company import Company
from scraper.utils import asyncRandomDelay, timed
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
import logging
from scraper.job import Job
from scraper.jobScrapeResult import JobScrapeResult
from tqdm.asyncio import tqdm


logger = logging.getLogger(__name__)


def getLocator(page: Page, company: Company, key: str) -> Locator:
        locDummy = page.locator('//h1/h1/h1/h1')
        xpath = company.xpaths[key]
        return page.locator(xpath) if xpath else locDummy


@timed('getAllJobs', debugOnly=False)
async def asyncGetAllJobDetails(browser: Browser, companies: defaultdict, jobUrls: List[Tuple[str, str]]) -> list[Job]:  
    #get maximum of X urls per company
    MAX_COMPANY_COUNT = 100
    companyCount = defaultdict(int)
    uniqueUrls = set()
    urlsToScrape = []
    for companyName, jobUrl in jobUrls:
        if jobUrl not in uniqueUrls and companyCount[companyName] < MAX_COMPANY_COUNT:
            companyCount[companyName] += 1
            uniqueUrls.add(jobUrl)
            urlsToScrape.append((companyName, jobUrl))

    #limit semaphore and split into coroutines
    semaphore = asyncio.Semaphore(8)
    jobScrapeResults = await tqdm.gather(
        *(asyncGetJobDetails(browser, companies[companyName], jobUrl, semaphore) 
          for companyName, jobUrl in urlsToScrape
        )
    )

    #print stats for positive scrape results
    for result in jobScrapeResults:
        if not result.job:
            companyCount[result.company.name] -= 1

    logger.info(
        '%s\nSuccessful Scrapes: %d',
        '\n'.join(
            f'{company}: {count}'
            for company, count in companyCount.items()
        ),
        sum(companyCount.values())
    )

    return [result.job for result in jobScrapeResults if result.job]


async def asyncGetJobDetails(browser: Browser, company: Company, url: str, semaphore: Semaphore) -> JobScrapeResult:
    async with semaphore:
        page = await browser.new_page()        
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        try:
            response = await page.goto(url)
            await asyncRandomDelay(shortDelay=True)

            if response is None:
                logger.warning('No response @ %d. Skipping.', url)
                return JobScrapeResult(None, company)
            if response.status != 200:
                logger.warning('Status %d @ %s. Skipping.', response.status, url)
                return JobScrapeResult(None, company)

            await page.locator(company.xpaths['jobTitle']).first.wait_for(timeout=5000) 
            locTitle = getLocator(page, company, 'jobTitle')
            locOffices = getLocator(page, company, 'location')
            locRemote = getLocator(page, company, 'remote')
            locDatePosted = getLocator(page, company, 'datePosted')

            title = await asyncGetLocatorText(locTitle, onlyFirst=True)   
            jobDesc = await asyncGetJobDesc(page, company)
            offices = await asyncGetLocatorText(locOffices)
            remote = await asyncGetLocatorText(locRemote)
            datePosted = await asyncGetLocatorText(locDatePosted)

            job = Job(url, company.id, company.name, title, jobDesc, offices, remote, datePosted)

            return JobScrapeResult(job, company)
        except PlaywrightTimeoutError:
            logger.warning('PlaywrightTimeoutError @ %s. Skipping.', url)
            return JobScrapeResult(None, company)
        finally:
            await page.close()


async def asyncGetLocatorText(locator: Locator, onlyFirst: bool=False):
    if onlyFirst:
        return await locator.nth(0).inner_text() if await locator.count() > 0 else None
    else:
        return ' \n\n '.join(await locator.all_inner_texts()) if await locator.count() > 0 else None


async def asyncGetJobDesc(page: Page, company: Company) -> str:
    sections = company.xpaths['jobDesc']
    sectionTexts = []

    try:
        for section in sections:
            sectionTexts.append(await asyncGetLocatorText(page.locator(section), True))
    except PlaywrightTimeoutError:
        return 
    
    return '\n\n'.join(text for text in sectionTexts if text)