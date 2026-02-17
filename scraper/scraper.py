from dataLoader import loadExistingDatabaseData, loadJson
from jobUrls import getAllJobUrls
from jobDetails import getAllJobDetails
from exportDetails import writeJobDetailsToFile, insertJobsToDatabase
from utils import setupLogging, emailLogging
import time
from playwright.sync_api import sync_playwright


def main():    
    dbCompanies, dbJobUrls = loadExistingDatabaseData()
    urlRenderTypes, xpaths = loadJson()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        jobUrls = getAllJobUrls(dbCompanies, page, urlRenderTypes, xpaths)
        jobDetails = getAllJobDetails(dbJobUrls, page, jobUrls, xpaths)
    
    writeJobDetailsToFile(jobDetails)
    insertJobsToDatabase(jobDetails)
    return


if __name__ == '__main__':
    timeStart = time.perf_counter()
    print('.\n.\n.\n.\n.\n')

    logger, jobActivity, timestamp = setupLogging()
        
    main()

    timeEnd = time.perf_counter()
    programTime = timeEnd - timeStart
    from utils import totalDelay
    print(f'Total Delay: {totalDelay}')
    print(f'Program Time: {programTime}')

    emailLogging(timestamp, programTime, jobActivity)
