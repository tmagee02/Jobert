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
# Fintech: Brex, Ramp, Robinhood, Chime, Mercury
# Infrastructure: Snowflake, Datadog, Cloudflare, Confluent
# Consumer: Snap, Discord, Pintrest, Instacart, Doordash, Reddit, Spotify
# DevTools: Vercel, Figma, Linear, Notion


def main():
    ID = 10
    NAME = 'Spotify'
    BASE_URL = 'https://www.lifeatspotify.com'
    SEARCH_PATH = '/jobs/'
    SEARCH_QUERY = '?l=new-york&l=boston&l=los-angeles&l=miami&l=washington-d-c&c=backend&c=client-c&c=data&c=developer-tools-infrastructure&c=engineering-leadership&c=machine-learning&c=mobile&c=network-engineering-it&c=security&c=tech-research&c=web'
    PAGINATION_TYPE = 'Show More'
    URL_ATTRIBUTE_TYPE = 'data-info'
    JOB_URL = "//div[@class='row']/div/div[@role='link']"
    PAGINATION = "//main//div[4]/div[@class='row']/following-sibling::div/div[1]/button"
    JOB_TITLE = '//main//h1'
    JOB_DESC = '//main/div/div[1]/div[2]/div'
    LOCATION = '//main/div/div[1]/div[2]/div/div[1]/div[3]/span'
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