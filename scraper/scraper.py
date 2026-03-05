from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import getAllJobUrls
from scraper.jobDetails import getAllJobDetails
from scraper.exportDetails import writeJobDetailsToFile, insertJobsToDatabase
from scraper.utils import setupLogging, emailLogging, totalDelay
import time
from playwright.sync_api import sync_playwright
from scraper.handleNLP import handleAllNLP


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

        handleAllNLP(jobDetails)

        for job in jobDetails.values():
            print('\n', job.url)
            print(f'{job.minSalary}, {job.maxSalary} : SALARY')
            print(f'{job.minExperience}, {job.maxExperience} : EXPERIENCE')
            for location in job.locations:
                print(f'{location} : LOCATION')

    
    # writeJobDetailsToFile(jobDetails)
    # insertJobsToDatabase(jobDetails)
    return


if __name__ == '__main__':
    timeStart = time.perf_counter()
    print('.\n.\n.\n.\n.\n')

    logger, jobActivity, timestamp = setupLogging()
        
    main()

    timeEnd = time.perf_counter()
    programTime = timeEnd - timeStart
    
    print(f'Total Delay: {totalDelay}')
    print(f'Program Time: {programTime}')

    emailLogging(timestamp, programTime, jobActivity)
