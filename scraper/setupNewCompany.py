from playwright.sync_api import sync_playwright
from collections import defaultdict
from pandas import DataFrame
from scraper.dataLoader import loadExistingDatabaseData
from scraper.jobUrls import getAllJobUrls
from scraper.jobDetails import getAllJobDetails
from scraper.exportDetails import writeJobDetailsToFile
from scraper.handleNLP import handleAllNLP
from scraper.company import Company


# Possible new companies:
# FAANG: Meta, Amazon?, Netfix, Google, + NVIDIA
# AI: Anthropic, xAI, Hugging Face, Cohere
# Fintech: *Plaid, *Brex, Ramp, Robinhood, Chime, Mercury
# Infrastructure: Snowflake, Datadog, Cloudflare, Confluent
# Consumer: Snap, Discord, Pintrest, Instacart, Doordash, Reddit, *Spotify
# DevTools: Vercel, Figma, Linear, Notion
# Misc.: Waymo, Wing (Google subsidiaries)

def main():
    ID = 10
    NAME = 'Google'
    BASE_URL = 'https://www.google.com'
    SEARCH_PATH = '/about/careers/applications/jobs/results/'
    SEARCH_QUERY = '?q="Software%20Engineer"&hl=en&location=United%20States&sort_by=date'
    PAGINATION_TYPE = None
    URL_ATTRIBUTE_TYPE = 'href'
    JOB_URL = "//main//ul//a"
    PAGINATION = None
    JOB_TITLE = '//span/div[1]/div/h2'
    JOB_DESC = '//c-wiz[1]//main//c-wiz/div/div/div/span/div[1]'
    LOCATION = '//span/div/div/span[2]/span'
    REMOTE = None
    DATE_POSTED = None
    XPATHS = {
            "jobUrl" : JOB_URL,
            "pagination" : PAGINATION,
            "jobTitle" : JOB_TITLE,
            "jobDesc" : JOB_DESC,
            "location" : LOCATION,
            "remote" : REMOTE,
            "datePosted" : DATE_POSTED
    }
    company = Company(ID, NAME, BASE_URL, SEARCH_PATH, SEARCH_QUERY, PAGINATION_TYPE, URL_ATTRIBUTE_TYPE, XPATHS)
    print(company.name, company.baseUrl, company.searchPath)
    companies = {NAME: company}
    dbJobUrls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        jobUrls = getAllJobUrls(companies, page)
        jobDetails = getAllJobDetails(dbJobUrls, page, jobUrls, companies)
        handleAllNLP(jobDetails)
        jobDetails = list(jobDetails.values())
        print(jobDetails[0].minSalary)

    writeJobDetailsToFile(jobDetails)
    return


if __name__ == '__main__':
    main()