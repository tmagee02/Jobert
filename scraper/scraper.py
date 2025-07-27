from dataLoader import loadExistingDatabaseData, loadJson
from jobUrls import getJobUrls
from jobDetails import getJobDetails
from exportDetails import writeJobDetailsToFile, insertJobToDatabase
from utils import randomDelay, setupLogging
import os
import time
import logging
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def main():    
    dbCompanies, dbJobUrls = loadExistingDatabaseData()
    urlRenderTypes, xpaths = loadJson()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

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

        jobDetails = {}
        count = 1
        for company, idCompany, jobUrl in jobUrls:
            if jobUrl not in dbJobUrls and jobUrl not in jobDetails:
                status = page.goto(jobUrl).status
                print(count)
                count += 1
                getJobDetails(page, status, xpaths, company, idCompany, jobDetails, jobUrl)
            else:
                logger.info(f'Job details already gathered for {jobUrl}. Skipping.')

        writeJobDetailsToFile(jobDetails)
        insertJobToDatabase(jobDetails)
    return


if __name__ == '__main__':
    timeStart = time.perf_counter()
    print('.\n.\n.\n.\n.\n')

    logger = setupLogging()
        
    main()

    timeEnd = time.perf_counter()
    programTime = timeEnd - timeStart
    from utils import totalDelay
    print(f'Total Delay: {totalDelay}')
    print(f'Program Time: {programTime}')

    # sendEmail(timestamp, programTime, loggerFile)
