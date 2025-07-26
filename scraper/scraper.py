from datetime import datetime
import os
import time
import random
import logging
import sqlite3
import json
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page, Locator
from urllib.parse import urljoin


def main():    
    selectCompany = '''
        select * 
        from Company
        '''

    with sqlite3.connect('./db/jobert.db') as conn:
        dataframe = pd.read_sql_query(selectCompany, conn)
        print(dataframe)
    
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

        for row in dataframe.itertuples():
            idCompany = row.id
            companyName = row.company_name
            baseUrl = row.base_url
            searchPath = row.search_path
            searchQuery = row.search_query
            urlRenderType = urlRenderTypes[companyName]
            # xJobUrl = xpaths[companyName]['jobUrl']
            # xNextPage = xpaths[companyName]['nextPage']
            # xJobTitle = xpaths[companyName]['jobTitle']
            # xJobDesc = xpaths[companyName]['jobDesc']
            # xLocation = xpaths[companyName]['location']
            # xRemote = xpaths[companyName]['remote']
            # xDatePosted = xpaths[companyName]['datePosted']
            
            page.goto(baseUrl + searchPath + searchQuery)
            randomDelay()
            jobUrls = getJobUrls(page, xpaths, companyName, baseUrl, searchPath, urlRenderType)
            for jobUrl in jobUrls:
                print(companyName, jobUrl)
        # page.goto(baseUrl + searchPath + query)
        # randomDelay()
        # html = page.inner_html('body')
        # jobUrls = getJobUrls(html)

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


def getJobUrls(page: Page, xpaths: dict, companyName: str, baseUrl: str, searchPath: str, urlRenderType: str) -> list[str]:
    jobUrls = []

    if urlRenderType == "Show More":
        buttonShowMore = page.locator(xpaths[companyName]['nextPage'])
        while buttonShowMore.count() > 0:
            buttonShowMore.click()
            try:
                randomDelay(True)
                page.locator(xpaths[companyName]['nextPage']).wait_for(timeout=5000)
                buttonShowMore = page.locator(xpaths[companyName]['nextPage'])
                print("button found")
            except:
                break

    elements = page.query_selector_all(xpaths[companyName]['jobUrl'])
    for e in elements:
        jobPath = e.get_attribute('href')        
        jobUrls.append(urljoin(baseUrl + searchPath, jobPath))

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
                    jobUrls.append(urljoin(baseUrl + searchPath, jobPath))

                page.locator(xpaths[companyName]['nextPage']).wait_for(timeout=5000)
                print("button found")

                maxPages -= 1
                buttonNextPage = page.locator(xpaths[companyName]['nextPage'])
            except:
                break

    print(len(jobUrls))
    return jobUrls


def getJobDetails(html: str, jobDetails: dict, jobUrl: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    jobTitle = soup.find('h1', class_='Copy__title').get_text(strip=True)
    jobDesc = soup.find('div', class_='RowLayout').get_text(separator=' \n ', strip=True)

    offices = soup.find('p', string='Office locations')
    remote = soup.find('p', string='Remote locations')
    if offices:
        offices = offices.find_next_sibling('p').get_text()
    if remote:
        remote = remote.find_next_sibling('p').get_text()

    jobDetails[jobUrl] = (jobTitle, jobDesc, offices, remote)
    return


def insertJobToDatabase(jobDetails: dict, idCompany: int) -> None:
    with sqlite3.connect('./db/jobert.db') as conn:
        cursor = conn.cursor()
        for jobUrl, (title, jobDesc, offices, remote) in jobDetails.items():
            insertJob = '''
                insert into Job (job_url, title, job_desc, company_id)
                values (?, ?, ?, ?)
                '''
            try:
                cursor.execute(insertJob, (jobUrl, title, jobDesc, idCompany))
                logger.info(f'Inserting row into db for Job: {title}. Good.')
                idJob = cursor.lastrowid
            except sqlite3.IntegrityError:
                logger.info(f'Row in db for Job: {title} already exists. Skipping.')
    return


#--------------------------------


def randomDelay(shortDelay: bool=False) -> None:
    randomTime = random.uniform(0.5, 1.5) if shortDelay else random.uniform(1.5, 5)
    logger.debug(f'Random Delay: {randomTime} sec')
    time.sleep(randomTime)
    return


def writeJobDetailsToFile(jobDetails: dict) -> None:
    with open('./scraper/jobDetails.txt', 'w') as f:
        for jobUrl, (title, jobDesc, offices, remote) in jobDetails.items():
            f.write(jobUrl)
            f.write(f'\n{title}\n')
            if offices:
                f.write(f'Office Locations: {offices}\n')
            if remote:
                f.write(f'Remote Locations: {remote}\n')
            f.write('\n')
            f.write(jobDesc)
            f.write('\n\n--------------------\n--------------------\n--------------------\n\n')
    return


def isClickable(buttonNextPage: Locator) -> bool:
    isRemoved = buttonNextPage.count() == 0
    isDisabled = buttonNextPage.get_attribute('disabled') is not None
    return not (isRemoved or isDisabled)


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
