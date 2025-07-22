import time
import random
import logging
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def main():
    '''
    create a json to handle the following for each scraped website:
    company name
    base url
    path (for the job search)
    query (to specify Software Engineer, location, etc)
    the requirements to find the correct links (only job links)
    etc.

    '''
    baseUrl = "https://stripe.com"
    path = "/jobs/search"
    query = "?query=Software+Engineer&remote_locations=North+America--US+Remote&office_locations=North+America--Atlanta&office_locations=North+America--Chicago&office_locations=North+America--New+York&office_locations=North+America--New+York+Privy+HQ&office_locations=North+America--San+Francisco+Bridge+HQ&office_locations=North+America--Seattle&office_locations=North+America--South+San+Francisco&office_locations=North+America--Washington+DC"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto(baseUrl + path + query)
        randomDelay()
        html = page.inner_html('body')
        jobUrls = getJobUrls(html, baseUrl)
        print(len(jobUrls), "\n", jobUrls)


    return


def getJobUrls(html: str, baseUrl: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    jobs = soup.find_all("a", class_="Link JobsListings__link")
    jobUrls = []

    for job in jobs:
        jobUrl = baseUrl + job.get("href")
        jobUrls.append(jobUrl)
    
    return jobUrls


'''
before getting job details, i should learn about response vs session
'''
def getJobDetails():
    return

def randomDelay():
    randomTime = random.uniform(1.5, 7)
    logger.info(randomTime)
    time.sleep(randomTime)



    
if __name__ == "__main__":
    print(".\n.\n.\n.\n.\n")
    logger = logging.getLogger("Jobert Scraper")
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.ERROR)
    main()
