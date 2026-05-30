from scraper.dataLoader import loadJson, loadExistingDatabaseData
from scraper.jobUrls import getAllJobUrls
from scraper.jobDetails import getJobDetails
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from collections import defaultdict
import json
import re


def main():
    companies = {'Brex'}
    dbCompanies, _ = loadExistingDatabaseData()
    dbCompanies = dbCompanies[dbCompanies['company_name'].isin(companies)]
    paginationTypes, xpaths = loadJson()
    print(dbCompanies, paginationTypes)

    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        jobUrls = getAllJobUrls(dbCompanies, page, paginationTypes, xpaths)
        
        jobDetails = {}
        count = 1
        companyCount = defaultdict(int)
        for company, idCompany, jobUrl in jobUrls:
            if jobUrl not in jobDetails and companyCount[company] < 25:
                try:
                    status = page.goto(jobUrl).status
                    print(count, jobUrl)
                    count += 1
                    companyCount[company] += 1
                    getJobDetails(page, status, xpaths, company, idCompany, jobDetails, jobUrl)
                except PlaywrightTimeoutError:
                    print(f'Possible invalid job @ {jobUrl}.')
            else:
                print(f'Either copy of prev url or already enough jobs. Skipping.')

    trainingData = setTrainingData(dbCompanies, jobDetails)

    with open('./scraper/nlp/trainingData.json', 'w', encoding="utf-8") as file: #encoding and ensureascii added to keep actual characters in json
        json.dump(trainingData, file, ensure_ascii=False, indent=4)
    return


def setTrainingData(dbCompanies, jobDetails):
    trainingData = []
    for url, job in jobDetails.items():
        #get company by id
        companyName = dbCompanies.loc[dbCompanies['id'] == job.idCompany, 'company_name'].iloc[0]

        #replace any /n, /t, etc. with spaces
        jobDesc, offices, remote = job.jobDesc, job.offices, job.remote
        if jobDesc: jobDesc = re.sub(r"\s+", " ", jobDesc)
        if offices: offices = re.sub(r"\s+", " ", offices)
        if remote: remote = re.sub(r"\s+", " ", remote)

        #join into one string
        jobDesc = f'{str(offices)} ::: {str(remote)}  <><><><>  {str(jobDesc)}'

        trainingData.append({
            'company' : companyName,
            'jobUrl' : url,
            'jobDesc' : jobDesc,
            'entities' : []
        })
    return trainingData

if __name__ == '__main__':
    main()