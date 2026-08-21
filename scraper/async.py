from playwright.async_api import async_playwright
import asyncio
import random
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import asyncCollectAllCompanyJobUrls
from scraper.jobDetails import asyncGetAllJobDetails
from scraper.handleNLP import handleAllNLP
from scraper.utils import timed, emailJobsInExperienceRange
from scraper.exportDetails import writeJobDetailsToFile, insertJobsToDatabase
import requests


@timed('Program')
async def main():
    companies, oldJobUrls = loadExistingDatabaseData()
    loadJson(companies)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)

        jobUrls = await asyncCollectAllCompanyJobUrls(browser, companies, oldJobUrls)
        jobsScraped = await asyncGetAllJobDetails(browser, companies, jobUrls)

        await browser.close()

    handleAllNLP(jobsScraped) # New Uber (maybe Stripe? untested) NLP salary bad (maybe experience? untested)
    shuffledJobs = list(jobsScraped)
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
    requests.post('https://ntfy.sh/jobert_scraper', data='poop!')
    return


if __name__ == '__main__':
    print('.\n.\n.\n.\n.\n.\n')
    asyncio.run(main())
