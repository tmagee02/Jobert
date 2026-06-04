from typing import Tuple
from scraper.utils import randomDelay
from playwright.sync_api import Page, Locator
from urllib.parse import urljoin, urlparse
import time
from scraper.company import Company

def getJobUrls(page: Page, company: Company) -> list[Tuple[str, str]]:
    jobUrls = []

    paginationLimit = 10
    paginationButton = page.locator(company.xpaths['pagination'])
    while paginationLimit > 0 and company.paginationType and isClickable(paginationButton):
        paginationButton.click()
        try:
            randomDelay(True)
            
            if company.paginationType == 'Next Page': 
                jobUrls.extend(getVisibleUrls(page, company))
            page.locator(company.xpaths['pagination']).wait_for(timeout=5000)

            paginationLimit -= 1
            paginationButton = page.locator(company.xpaths['pagination'])
        except: 
            break
    
    if company.paginationType != 'Next Page':
        jobUrls = getVisibleUrls(page, company)

    print(f'{company.name}: {len(jobUrls)}')
    return jobUrls


def getAllJobUrls(companies: dict, page: Page) -> list[Tuple[str, str]]:
    timeStart = time.perf_counter()
    jobUrls = []

    print(f'\nNumber of Possible Company URLs:')
    for company in companies.values():
        page.goto(company.searchUrl())
        randomDelay()
        companyJobUrls = getJobUrls(page, company)
        jobUrls.extend(companyJobUrls)

    timeEnd = time.perf_counter()
    timeGetAllJobUrls = timeEnd - timeStart
    print(f'\ngetAllJobUrls Time: {timeGetAllJobUrls}\n')
    return jobUrls


def isClickable(paginationButton: Locator) -> bool:
    isRemoved = paginationButton.count() == 0
    isDisabled = paginationButton.get_attribute('disabled') is not None
    return not (isRemoved or isDisabled)


def getVisibleUrls(page: Page, company: Company) -> list[Tuple[str, str]]:
    visibleUrls = []
    elements = page.locator(company.xpaths['jobUrl'])
    for i in range(elements.count()):
        element = elements.nth(i)
        jobPath = element.get_attribute(company.urlAttributeType)
        jobPath = normalizeJobPath(company.searchPath, jobPath)

        visibleUrls.append((company.name, urljoin(company.baseUrl + company.searchPath, jobPath)))
    return visibleUrls


'''
Removes any duplication between the searchPath suffix and jobPath 
prefix if jobPath is not an absolute path

ex. Google searchPath and jobPath overlap
'''
def normalizeJobPath(searchPath: str, jobPath: str) -> str:
    if urlparse(jobPath).scheme:
        return jobPath

    search = [component for component in searchPath.split('/') if component]
    job = [component for component in jobPath.split('/') if component]

    common = 0
    for i in range(min(len(search), len(job)), 0, -1):
        if search[-i:] == job[:i]:
            common = i
            break
    
    return '/'.join(job[common:])
    