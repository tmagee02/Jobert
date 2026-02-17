from typing import List, Tuple
from utils import randomDelay
from playwright.sync_api import Page, Locator
from urllib.parse import urljoin
from pandas import DataFrame
from collections import defaultdict
import time


def getJobUrls(page: Page, xpaths: dict, companyName: str, idCompany: int, baseUrl: str, searchPath: str, urlRenderType: str) -> list[(str, str)]:
    jobUrls = []

    if urlRenderType == "Show More":
        maxExtensions = 14
        buttonShowMore = page.locator(xpaths[companyName]['nextPage'])
        while maxExtensions > 0 and buttonShowMore.count() > 0:
            buttonShowMore.click()
            try:
                randomDelay(True)
                page.locator(xpaths[companyName]['nextPage']).wait_for(timeout=5000)

                maxExtensions -= 1
                buttonShowMore = page.locator(xpaths[companyName]['nextPage'])
            except:
                break

    elements = page.query_selector_all(xpaths[companyName]['jobUrl'])
    for e in elements:
        jobPath = e.get_attribute('href')        
        jobUrls.append((companyName, idCompany, urljoin(baseUrl + searchPath, jobPath)))

    if urlRenderType == "Next Page":
        maxPages = 9
        buttonNextPage = page.locator(xpaths[companyName]['nextPage'])
        while maxPages > 0 and isClickable(buttonNextPage):
            buttonNextPage.click()
            try:
                randomDelay(True)
                elements = page.query_selector_all(xpaths[companyName]['jobUrl'])
                for e in elements:
                    jobPath = e.get_attribute('href')        
                    jobUrls.append((companyName, idCompany, urljoin(baseUrl + searchPath, jobPath)))

                page.locator(xpaths[companyName]['nextPage']).wait_for(timeout=5000)
                # print("button found")

                maxPages -= 1
                buttonNextPage = page.locator(xpaths[companyName]['nextPage'])
            except:
                break

    print(len(jobUrls))
    return jobUrls


def isClickable(buttonNextPage: Locator) -> bool:
    isRemoved = buttonNextPage.count() == 0
    isDisabled = buttonNextPage.get_attribute('disabled') is not None
    return not (isRemoved or isDisabled)


def getAllJobUrls(dbCompanies: DataFrame, page: Page, urlRenderTypes: dict, xpaths: defaultdict) -> List[Tuple[str, int, str]]:
    timeStart = time.perf_counter()
    jobUrls = []

    for row in dbCompanies.itertuples():
        idCompany = row.id
        companyName = row.company_name
        baseUrl = row.base_url
        searchPath = row.search_path
        searchQuery = row.search_query
        urlRenderType = urlRenderTypes[companyName]
        
        page.goto(baseUrl + searchPath + searchQuery)
        randomDelay()
        companyJobUrls = getJobUrls(page, xpaths, companyName, idCompany, baseUrl, searchPath, urlRenderType)
        jobUrls.extend(companyJobUrls)

    timeEnd = time.perf_counter()
    timeGetAllJobUrls = timeEnd - timeStart
    print(f'\ngetAllJobUrls Time: {timeGetAllJobUrls}\n')
    return jobUrls