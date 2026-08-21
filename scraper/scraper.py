from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.job import Job
from scraper.jobUrls import collectAllCompanyJobUrls
from scraper.jobDetails import getAllJobDetails
from scraper.exportDetails import writeJobDetailsToFile, insertJobsToDatabase
from scraper.utils import setupLogging, emailLogging, emailJobsInExperienceRange, totalDelay
import time
from playwright.sync_api import sync_playwright
from scraper.handleNLP import handleAllNLP
import random


def main():    
    # emailJobsInExperienceRange([Job('www.google.com', 100, 'test', 'test', None, None, None, 0, 500, 0, 500, ['test1, test2'])], 0, 2)
    companies, oldJobUrls = loadExistingDatabaseData()
    loadJson(companies)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        jobUrls = collectAllCompanyJobUrls(page, companies, oldJobUrls)
        jobDetails = getAllJobDetails(page, companies, jobUrls)

        handleAllNLP(jobDetails)
        shuffledJobs = list(jobDetails.values())
        random.shuffle(shuffledJobs)

        # for job in shuffledJobs:  
        #     print('\n', job.url)
        #     print(f'{job.minSalary}, {job.maxSalary} : SALARY')
        #     print(f'{job.minExperience}, {job.maxExperience} : EXPERIENCE')
        #     for location in job.locations:
        #         print(f'{location} : LOCATION')

    emailJobsInExperienceRange(shuffledJobs, 0, 2)
    writeJobDetailsToFile(shuffledJobs)
    insertJobsToDatabase(shuffledJobs)
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
