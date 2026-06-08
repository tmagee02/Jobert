from playwright.sync_api import sync_playwright
from scraper.jobUrls import collectAllCompanyJobUrls
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
    NAME = 'Datadog'
    BASE_URL = 'https://careers.datadoghq.com'
    SEARCH_PATH = '/all-jobs/'
    SEARCH_QUERY = '?parent_department_Engineering%5B0%5D=Engineering&region_Americas%5B0%5D=Americas'
    URL_DISCOVERY_STRATEGY = [
    ]
    PAGINATION_TYPE = 'Next Page'
    URL_ATTRIBUTE_TYPE = 'href'
    JOB_URL = '//button/a'
    PAGINATION = '//a[@aria-label="Next Page"]'
    JOB_TITLE = '//main/h2'
    JOB_DESC = [
        '//div[@class="job-description"]'
    ]
    LOCATION = '//main/div/p'
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
    company = Company(
        id=ID, 
        name=NAME, 
        baseUrl=BASE_URL, 
        searchPath=SEARCH_PATH, 
        searchQuery=SEARCH_QUERY, 
        urlDiscoveryStrategy=URL_DISCOVERY_STRATEGY,
        paginationType=PAGINATION_TYPE, 
        urlAttributeType=URL_ATTRIBUTE_TYPE, 
        xpaths=XPATHS
    )
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

        jobUrls = collectAllCompanyJobUrls(companies, page)
        jobDetails = getAllJobDetails(dbJobUrls, page, jobUrls, companies)
    

    handleAllNLP(jobDetails)
    jobDetails = list(jobDetails.values())
    for job in jobDetails:
        print(job.title, job.minSalary, job.maxSalary, job.minExperience, job.maxExperience, sep=" | ")

    writeJobDetailsToFile(jobDetails)
    return


if __name__ == '__main__':
    main()
