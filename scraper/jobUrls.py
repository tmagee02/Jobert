from scraperUtils import randomDelay
from playwright.sync_api import Page, Locator
from urllib.parse import urljoin


def getJobUrls(page: Page, xpaths: dict, companyName: str, baseUrl: str, searchPath: str, urlRenderType: str) -> list[(str, str)]:
    jobUrls = []

    if urlRenderType == "Show More":
        buttonShowMore = page.locator(xpaths[companyName]['nextPage'])
        while buttonShowMore.count() > 0:
            buttonShowMore.click()
            try:
                randomDelay(True)
                page.locator(xpaths[companyName]['nextPage']).wait_for(timeout=5000)
                buttonShowMore = page.locator(xpaths[companyName]['nextPage'])
                # print("button found")
            except:
                break

    elements = page.query_selector_all(xpaths[companyName]['jobUrl'])
    for e in elements:
        jobPath = e.get_attribute('href')        
        jobUrls.append((companyName, urljoin(baseUrl + searchPath, jobPath)))

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
                    jobUrls.append((companyName, urljoin(baseUrl + searchPath, jobPath)))

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