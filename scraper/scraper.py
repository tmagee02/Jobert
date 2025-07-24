from datetime import datetime
import os
import time
import random
import logging
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def main():
    selectCompany = '''
        select * 
        from Company
        '''

    with sqlite3.connect('./db/jobert.db') as conn:
        dataframe = pd.read_sql_query(selectCompany, conn)
        print(dataframe)

    idCompany = int(dataframe.at[0, 'id'])
    companyName = dataframe.at[0, 'company_name']
    baseUrl = dataframe.at[0, 'base_url']
    searchPath = dataframe.at[0, 'search_path']
    query = dataframe.at[0, 'search_query']

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto(baseUrl + searchPath + query)
        randomDelay()
        html = page.inner_html('body')
        jobUrls = findJobUrls(html)

        jobDetails = {}
        for jobUrl in jobUrls:
            if jobUrl not in jobDetails:
                logger.info(f'Gathering job details for {jobUrl}. Good.')
                page.goto(jobUrl)
                page.locator('h1.Copy__title').first.wait_for(state='visible')
                html = page.inner_html('body')
                findJobDetails(html, jobDetails, jobUrl)
                randomDelay()
            else:
                logger.info(
                    f'Job details already gathered for {jobUrl}. Skipping.')

        writeJobDetailsToFile(jobDetails)
        insertJobToDatabase(jobDetails, idCompany)

    return


def findJobUrls(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    jobs = soup.find_all("a", class_="Link JobsListings__link")
    jobUrls = []

    for job in jobs:
        jobUrl = job.get("href")
        jobUrls.append(jobUrl)

    return jobUrls


def findJobDetails(html: str, jobDetails: dict, jobUrl: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    jobTitle = soup.find('h1', class_='Copy__title').get_text(strip=True)
    jobDesc = soup.find('div', class_='RowLayout').get_text(
        separator=' \n\n ', strip=True)

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
        for jobUrl, (title, jobDesc, offices, remote) in jobDetails.items():
            insertJob = '''
                insert into Job (job_url, title, job_desc, company_id)
                values (?, ?, ?, ?)
                '''
            try:
                conn.execute(insertJob, (jobUrl, title, jobDesc, idCompany))
                logger.info(f'Inserting row into db for Job: {title}. Good.')
            except sqlite3.IntegrityError:
                logger.info(f'Row in db for Job: {title} already exists. Skipping.')





def randomDelay() -> None:
    randomTime = random.uniform(1.5, 7)
    logger.debug(f'Random Delay: {randomTime} sec')
    time.sleep(randomTime)


def writeJobDetailsToFile(jobDetails: dict) -> None:
    with open('jobDetails.txt', 'w') as f:
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
