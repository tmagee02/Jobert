from playwright.sync_api import sync_playwright
from scraper.jobUrls import getAllJobUrls
from scraper.jobDetails import getAllJobDetails
from scraper.exportDetails import writeJobDetailsToFile
from scraper.handleNLP import handleAllNLP
from scraper.company import Company


# Possible new companies:
# Big Tech: Meta, Amazon?, Netfix, *Google, NVIDIA, *Apple 2
# AI: Anthropic, xAI, Hugging Face, Cohere, *OpenAI 1
# Fintech: *Plaid, *Brex, Ramp, Robinhood, Chime, Mercury, *Stripe, *Block 4
# Infrastructure: Snowflake, Datadog, Cloudflare, Confluent, *Databricks 1
# Consumer: Snap, Discord, Pintrest, Instacart, Doordash, Reddit, *Spotify, *Airbnb, *Uber 3
# DevTools: Vercel, Figma, Linear, Notion 0
# Misc.: Waymo, Wing (Google subsidiaries)

def main():
    ID = 12
    NAME = 'Anthropic'
    BASE_URL = 'https://www.anthropic.com'
    SEARCH_PATH = '/careers/jobs'
    SEARCH_QUERY = ''
    PAGINATION_TYPE = None
    URL_ATTRIBUTE_TYPE = 'href'
    JOB_URL = "//main//ul//a"
    PAGINATION = None
    JOB_TITLE = '//span/div[1]/div/h2'
    JOB_DESC = [
        "//span/div/div[4]",
        "//span/div/div[5]",
        "//span/div/div[6]",
    ]
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
    for job in jobDetails:
        print(job.title, job.minSalary, job.maxSalary, job.minExperience, job.maxExperience, sep=" | ")

    writeJobDetailsToFile(jobDetails)
    return


if __name__ == '__main__':
    main()