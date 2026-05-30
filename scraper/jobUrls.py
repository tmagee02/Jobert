from typing import Tuple
from scraper.utils import randomDelay
from playwright.sync_api import Page, Locator
from urllib.parse import urljoin
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
        jobUrls.extend(getVisibleUrls(page, company))

    print(f'{company.name}: {len(jobUrls)}')
    # print(jobUrls)
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
    elements = page.query_selector_all(company.xpaths['jobUrl'])
    for e in elements:
        jobPath = e.get_attribute('href')
        visibleUrls.append((company.name, urljoin(company.baseUrl + company.searchPath, jobPath)))
    return visibleUrls