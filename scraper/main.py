from playwright.async_api import async_playwright
import asyncio
import random
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import collectAllCompanyJobUrls
from scraper.scrapeJobs import scrapeAllJobs
from scraper.processNLP import processNLP
from scraper.utils import timed, emailJobsInExperienceRange, sendExperiencePushNotification, setupLogging
from scraper.exportDetails import writeJobDetailsToFile, insertJobsToDatabase


@timed('Program', debugOnly=False)
async def main():
    companies, oldJobUrls = loadExistingDatabaseData()
    loadJson(companies)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)

        jobUrls = await collectAllCompanyJobUrls(browser, companies, oldJobUrls)
        jobsScraped = await scrapeAllJobs(browser, companies, jobUrls)

        await browser.close()

    processNLP(jobsScraped)
    shuffledJobs = list(jobsScraped)
    random.shuffle(shuffledJobs)

    emailJobsInExperienceRange(shuffledJobs, 0, 2)
    writeJobDetailsToFile(shuffledJobs)
    insertJobsToDatabase(shuffledJobs)

    try:
        sendExperiencePushNotification(shuffledJobs, 0)
        sendExperiencePushNotification(shuffledJobs, 1)
    except Exception as e:
        print(f'Failed to send push notifications: {e}')
    return


if __name__ == '__main__':
    print('.\n.\n.\n.\n.\n.\n')
    setupLogging()
    asyncio.run(main())
