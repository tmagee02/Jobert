from jobUrls import getJobUrls
from jobDetails import getJobDetails
from exportDetails import writeJobDetailsToFile, insertJobToDatabase
from utils import randomDelay
from datetime import datetime
import os
import time
import logging
import sqlite3
import json
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def main():    
    qSelectCompany = '''
        select * 
        from Company
        '''
    qSelectJobUrls = '''
        select job_url
        from Job
        '''

    with sqlite3.connect('./db/jobert.db') as conn:
        df_companies = pd.read_sql_query(qSelectCompany, conn)
        print(df_companies)
        df_jobUrls = pd.read_sql_query(qSelectJobUrls, conn)
    
    dbJobUrls = set(df_jobUrls['job_url'])

    
    with open('./scraper/xpathCompany.json', 'r') as file:
        data = json.load(file)


    urlRenderTypes = {}
    xpaths = defaultdict(dict)
    for company in data:
        urlRenderTypes[company['companyName']] = company['urlRenderType']
        xpaths[company['companyName']] = company['xpaths']

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        jobUrls = []
        for row in df_companies.itertuples():
            idCompany = row.id
            companyName = row.company_name
            baseUrl = row.base_url
            searchPath = row.search_path
            searchQuery = row.search_query
            urlRenderType = urlRenderTypes[companyName]
            
            page.goto(baseUrl + searchPath + searchQuery)
            randomDelay()
            companyJobUrls = getJobUrls(page, xpaths, companyName, baseUrl, searchPath, urlRenderType)
            jobUrls.extend(companyJobUrls)

        jobDetails = {}
        for company, jobUrl in jobUrls:
            if jobUrl not in dbJobUrls and company == 'Airbnb':
                logger.info(f'Gathering job details for {jobUrl}. Good.')
                page.goto(jobUrl)
                #wait for title?
                getJobDetails(page, xpaths, company, jobDetails)
                randomDelay()
            else:
                logger.info(f'Job details already gathered for {jobUrl}. Skipping.')

            

        # jobDetails = {}
        # for jobUrl in jobUrls:
        #     if jobUrl not in jobDetails:
        #         logger.info(f'Gathering job details for {jobUrl}. Good.')
        #         page.goto(jobUrl)
        #         page.locator('h1.Copy__title').first.wait_for(state='visible')
        #         html = page.inner_html('body')
        #         exposeJobDetails()
        #         getJobDetails(html, jobDetails, jobUrl)
        #         randomDelay()
        #     else:
        #         logger.info(
        #             f'Job details already gathered for {jobUrl}. Skipping.')

        # writeJobDetailsToFile(jobDetails)
        # insertJobToDatabase(jobDetails, idCompany)

    return


if __name__ == '__main__':
    timeStart = time.perf_counter()
    print('.\n.\n.\n.\n.\n')

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    loggerFile = f'./logs/scraper_logs_{timestamp}.log'
    logger = logging.getLogger('Jobert Scraper')
    formatting = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=loggerFile, level=logging.DEBUG, format=formatting)
        
    main()

    timeEnd = time.perf_counter()
    programTime = timeEnd - timeStart
    print(f'Program Time: {programTime}')

    # sendEmail(timestamp, programTime, loggerFile)
