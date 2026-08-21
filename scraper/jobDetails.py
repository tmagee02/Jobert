import asyncio
from asyncio import Semaphore
from playwright.async_api import async_playwright, Playwright, Browser, TimeoutError
from typing import List, Tuple, Set
from collections import defaultdict
from scraper.company import Company
from scraper.utils import randomDelay, asyncRandomDelay, timed
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
import logging
import time
from scraper.job import Job
from scraper.jobScrapeResult import JobScrapeResult
from tqdm.asyncio import tqdm

def getLocator(page: Page, company: Company, key: str) -> Locator:
        locDummy = page.locator('//h1/h1/h1/h1')
        xpath = company.xpaths[key]
        return page.locator(xpath) if xpath else locDummy


# def getLocatorText(locator: Locator, onlyFirst: bool=False):
#     if onlyFirst:
#         return locator.nth(0).inner_text() if locator.count() > 0 else None
#     else:
#         return ' \n\n '.join(locator.all_inner_texts()) if locator.count() > 0 else None


# def getJobDetails(page: Page, status: int, company: Company, jobDetails: dict, url: str) -> None:
#     logger = logging.getLogger('Jobert Scraper')
#     jobActivity = logging.getLogger('Job Activity')
#     if status != 200:
#         logger.error(f'Status {status} @ {url}. Skipping.')
#         jobActivity.error(f'Status {status} @ {url}. Skipping.')
#         return

#     try:
#         logger.info(f'Status {status} @ {url}. Good.')
#         page.locator(company.xpaths['jobTitle']).nth(0).wait_for(timeout=5000)
#         locTitle = getLocator(page, company, 'jobTitle')
#         locOffices = getLocator(page, company, 'location')
#         locRemote = getLocator(page, company, 'remote')
#         locDatePosted = getLocator(page, company, 'datePosted')

#         title = getLocatorText(locTitle, onlyFirst=True)
#         jobDesc = getJobDesc(page, company)
#         offices = getLocatorText(locOffices)
#         remote = getLocatorText(locRemote)
#         datePosted = getLocatorText(locDatePosted)
        
#         randomDelay(True)
#         jobDetails[url] = Job(url, company.id, title, jobDesc, offices, remote, datePosted)
#         jobActivity.info(f'New job ( {title} ) found @ {url}')
#         return 
#     except PlaywrightTimeoutError:
#         logger.error(f'Possible invalid job @ {url}.')
#         jobActivity.error(f'Possible invalid job @ {url}.')
#         return


# def getAllJobDetails(page: Page, companies: defaultdict, jobUrls: List[Tuple[str, str]]) -> dict[str, Job]:  
#     counts = defaultdict(int)
#     for companyName, jobUrl in jobUrls:
#         counts[companyName] += 1

#     print(counts)
#     MAX_COMPANY_COUNT = 5
#     timeStart = time.perf_counter()
#     logger = logging.getLogger('Jobert Scraper')
#     jobActivity = logging.getLogger('Job Activity')
#     jobDetails = {}
#     count = 1
#     companyCount = defaultdict(int)
#     for companyName, jobUrl in jobUrls:
#         if jobUrl not in jobDetails and companyCount[companyName] < MAX_COMPANY_COUNT:
#             try:
#                 status = page.goto(jobUrl).status
#                 print(count, jobUrl)
#                 count += 1
#                 companyCount[companyName] += 1
#                 getJobDetails(page, status, companies[companyName], jobDetails, jobUrl)
#             except PlaywrightTimeoutError:
#                 logger.error(f'Possible invalid job @ {jobUrl}.')
#                 jobActivity.error(f'Possible invalid job @ {jobUrl}.')
#         else:
#             logger.info(f'Job details already gathered for {jobUrl}. Skipping.')
    
#     print('\nCompany URL Counts:')
#     for company, count in companyCount.items():
#         print(f'{company}: {count}')

#     timeEnd = time.perf_counter()
#     timeGetAllJobDetails = timeEnd - timeStart
#     print(f'\ngetAllJobDetails Time: {timeGetAllJobDetails}\n')
#     return jobDetails


# def getJobDesc(page: Page, company: Company) -> str:
#     sections = company.xpaths['jobDesc']
#     sectionTexts = []

#     try:
#         for section in sections:
#             sectionTexts.append(getLocatorText(page.locator(section), True))
#     except PlaywrightTimeoutError:
#         return 
    
#     return '\n\n'.join(text for text in sectionTexts if text)



#-------async
#-------async
#-------async
#-------async
#-------async
@timed('getAllJobs134')
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
    print(*(f'{company}: {count}' for company, count in companyCount.items()), f'Successful Scrapes: {sum(companyCount.values())}', sep='\n')

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
                print(f'No response @ {url}. Skipping')
                return JobScrapeResult(None, company)
            if response.status != 200:
                print(f'Status {response.status} @ {url}. Skipping.')
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
            print(f'\nPlaywrightTimeoutError @ {url}.')
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