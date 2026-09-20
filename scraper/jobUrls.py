import asyncio
import logging
from typing import Set, Tuple
from scraper.discoveryStrategy import runDiscoveryStrategy
from scraper.utils import randomDelay, timed
from playwright.sync_api import Page, Locator
from playwright.async_api import Browser, TimeoutError
from urllib.parse import urljoin, urlparse
from scraper.company import Company

logger = logging.getLogger(__name__)


'''
Removes any duplication between the searchPath suffix and jobPath 
prefix if jobPath is not an absolute path

ex. Google searchPath and jobPath overlap
'''
def normalizeJobPath(searchPath: str, jobPath: str) -> str:
    #absolute or root-relative
    if urlparse(jobPath).scheme or jobPath[0] == '/':
        return jobPath

    search = [component for component in searchPath.split('/') if component]
    job = [component for component in jobPath.split('/') if component]

    common = 0
    for i in range(min(len(search), len(job)), 0, -1):
        if search[-i:] == job[:i]:
            common = i
            break
    
    return '/'.join(job[common:])
    

def filterOldUrls(companyName: str, companyJobUrls: str, oldJobUrls: Set[str]):
    newUrls = []
    for company, url in companyJobUrls:
        if url not in oldJobUrls:
            newUrls.append((company, url))
    
    logger.debug(
        '%s: %d new urls | Ignoring %d previously obtained urls', 
        companyName, len(newUrls), 
        len(companyJobUrls) - len(newUrls)
        )
    return newUrls


@timed('collectAllCompanyJobUrls', debugOnly=False)
async def collectAllCompanyJobUrls(browser: Browser, companies: dict, oldJobUrls: Set[str]):
    jobUrls = []
    companyUrls = await asyncio.gather(*(collectCompanyUrls(browser, company, oldJobUrls) for company in companies.values()))

    for urls in companyUrls:
        jobUrls.extend(urls)

    logger.info('Total URLs: %d', len(jobUrls))
    return jobUrls


@timed('companyUrls')
async def collectCompanyUrls(browser: Browser, company: Company, oldJobUrls: Set[str]):
    page = await browser.new_page()        
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
    """)

    await page.goto(company.searchUrl())
    await randomDelay(shortDelay=True)
    await runDiscoveryStrategy(company, page)

    jobUrls = []
    paginationLimit = 9    
    paginationButton = page.locator(company.xpaths['pagination'])
    while paginationLimit > 0 and company.paginationType and await isClickable(paginationButton):
        if company.paginationType == 'Next Page': 
            jobUrls.extend(await getVisibleUrls(page, company))

        await paginationButton.click()
        await randomDelay(True)
        try:
            await page.locator(company.xpaths['pagination']).wait_for(timeout=5000)
            paginationLimit -= 1
        except TimeoutError: 
            break
    
    jobUrls.extend(await getVisibleUrls(page, company))

    await page.close()    
    
    jobUrls = filterOldUrls(company.name, jobUrls, oldJobUrls)
    return jobUrls


async def isClickable(paginationButton: Locator) -> bool:
    isRemoved = await paginationButton.count() == 0
    isDisabled = await paginationButton.get_attribute('disabled') is not None
    return not (isRemoved or isDisabled)


async def getVisibleUrls(page: Page, company: Company) -> list[Tuple[str, str]]:
    visibleUrls = []
    elements = page.locator(company.xpaths['jobUrl'])

    try:
        await elements.first.wait_for(timeout=30000)
    except TimeoutError:
        return []
    
    for i in range(await elements.count()):
        element = elements.nth(i)
        jobPath = await element.get_attribute(company.urlAttributeType)
        jobPath = normalizeJobPath(company.searchPath, jobPath)

        visibleUrls.append((company.name, urljoin(company.baseUrl + company.searchPath, jobPath)))
    return visibleUrls