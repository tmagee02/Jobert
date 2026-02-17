import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dataLoader import loadJson
from jobDetails import getLocator, getLocatorText

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from collections import defaultdict
import pandas as pd
import sqlite3
import json
import re


def main():
    qSelectCompanies = '''
        select company_name
        from Company
    '''
    _, xpaths = loadJson()

    urls = set()
    with sqlite3.connect('./db/jobert.db') as conn:
        dbCompanies = pd.read_sql_query(qSelectCompanies, conn)
        companies = set(dbCompanies['company_name'])
        
        for company in companies:
            qSelectFirstJobs = f'''
                select c.company_name, j.job_url, j.date_scraped
                from Job j
                join Company c on j.company_id = c.id
                where c.company_name = '{company}'
                order by j.date_scraped desc
                limit 25
            '''
            dbCompanyUrls = pd.read_sql_query(qSelectFirstJobs, conn)
            for url in dbCompanyUrls['job_url']:
                urls.add((company, url))

    print(len(urls))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)


        
        companyCount = defaultdict(int)
        trainingData = []
            
        for company, url in urls:
            status = page.goto(url).status
            if status != 200:
                print(status, company)
                continue

            try:

                page.locator(xpaths[company]['jobDesc']).nth(0).wait_for(timeout=5000)
                locJobDesc = getLocator(page, xpaths, company, 'jobDesc')
                locLocations = getLocator(page, xpaths, company, 'location')
                locRemote = getLocator(page, xpaths, company, 'remote')

                jobDesc = getLocatorText(locJobDesc)
                locations = getLocatorText(locLocations)
                remote = getLocatorText(locRemote)

                if jobDesc: jobDesc = re.sub(r"\s+", " ", jobDesc)
                if locations: locations = re.sub(r"\s+", " ", locations)
                if remote: remote = re.sub(r"\s+", " ", remote)
                

                '''
                trying to merge locations and remote into one
                '''
                locations = str(locations) + ' ::: ' + str(remote)


                print(bool(jobDesc), locations, remote)
                companyCount[company] += 1
                trainingData.append({
                    'company' : company,
                    'jobUrl' : url,
                    'jobDesc' : jobDesc,
                    'locations' : locations
                    # 'remote' : remote
                })
            except PlaywrightTimeoutError:
                print(f'L {company}')
        
        print(companyCount)
        with open('./scraper/nlp/trainingData.json', 'w', encoding="utf-8") as file: #encoding and ensureascii added to keep actual characters in json
            json.dump(trainingData, file, ensure_ascii=False, indent=4)
            

    return


if __name__ == '__main__':
    main()