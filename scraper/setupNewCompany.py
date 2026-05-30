from playwright.sync_api import sync_playwright
from collections import defaultdict
from pandas import DataFrame
from scraper.dataLoader import loadExistingDatabaseData
from scraper.jobUrls import getAllJobUrls
from scraper.jobDetails import getAllJobDetails
from scraper.exportDetails import writeJobDetailsToFile
from scraper.handleNLP import handleAllNLP


# Possible new companies:
# FAANG: Meta, Amazon?, Netfix, Google, + NVIDIA
# AI: Anthropic, xAI, Hugging Face, Cohere
# Fintech: Brex, Ramp, Robinhood, Chime, Mercury
# Infrastructure: Snowflake, Datadog, Cloudflare, Confluent
# Consumer: Snap, Discord, Pintrest, Instacart, Doordash, Reddit, Spotify
# DevTools: Vercel, Figma, Linear, Notion


def main():
    NEW_COMPANY = 'Brex'
    BASE_URL = 'https://www.brex.com/'
    SEARCH_PATH = '/careers'
    SEARCH_QUERY = '?department=Engineering&country=United+States'
    URL_RENDER_TYPE = None
    JOB_URL = '//h3/following-sibling::div//a'
    NEXT_PAGE = None
    JOB_TITLE = '//h1'
    JOB_DESC = '//main/div/div/div[2]/div'
    LOCATION = '//h4'
    REMOTE = None
    DATE_POSTED = None
    
    dbCompanies = DataFrame({
        'id': [1],
        'company_name': [NEW_COMPANY],
        'base_url': [BASE_URL],
        'search_path': [SEARCH_PATH],
        'search_query': [SEARCH_QUERY],
    })
    print(dbCompanies)
    dbJobUrls = set()
    urlRenderTypes = {
        NEW_COMPANY: URL_RENDER_TYPE
    }
    newCompanyXpaths = {
            "jobUrl" : JOB_URL,
            "nextPage" : NEXT_PAGE,
            "jobTitle" : JOB_TITLE,
            "jobDesc" : JOB_DESC,
            "location" : LOCATION,
            "remote" : REMOTE,
            "datePosted" : DATE_POSTED
    }
    xpaths = defaultdict(dict)
    xpaths[NEW_COMPANY] = newCompanyXpaths

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        jobUrls = getAllJobUrls(dbCompanies, page, urlRenderTypes, xpaths)
        jobDetails = getAllJobDetails(dbJobUrls, page, jobUrls, xpaths)
        handleAllNLP(jobDetails)
        jobDetails = list(jobDetails.values())
        print(jobDetails[0].minSalary)

        # for job in jobDetails:
        #     print(job.title, job.minSalary, job.maxSalary, job.minExperience, job.maxExperience, '\n', job.jobDesc[-700:])

    writeJobDetailsToFile(jobDetails)
    return


if __name__ == '__main__':
    main()