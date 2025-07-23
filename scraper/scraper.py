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
        jobUrls = findJobUrls(html)
        # print(len(jobUrls), "\n", jobUrls)
        jobDetails = {}
        for jobUrl in jobUrls:
            if jobUrl not in jobDetails:
                logger.info(f'Gathering job details for {jobUrl}')
                page.goto(jobUrl)
                page.locator('h1.Copy__title').first.wait_for(state='visible')
                html = page.inner_html('body')
                findJobDetails(html, jobDetails, jobUrl)
                randomDelay()
            else:
                logger.info(f'Job details already gathered for {jobUrl}. Skipping.')
        
        writeJobDetailsToFile(jobDetails)

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
    jobDesc = soup.find('div', class_='RowLayout').get_text(separator=' \n\n ', strip=True)

    offices = soup.find('p', string='Office locations')
    remote = soup.find('p', string='Remote locations')
    if offices:
        offices = offices.find_next_sibling('p').get_text()
    if remote:
        remote = remote.find_next_sibling('p').get_text()

    jobDetails[jobUrl] = (jobTitle, jobDesc, offices, remote)
    return


def randomDelay():
    randomTime = random.uniform(1.5, 7)
    logger.debug(randomTime)
    time.sleep(randomTime)


def writeJobDetailsToFile(jobDetails: dict):        
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
    print('.\n.\n.\n.\n.\n')
    logger = logging.getLogger('Jobert Scraper')
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.ERROR)
    timeStart = time.perf_counter()
    main()
    timeEnd = time.perf_counter()
    programTime = timeEnd - timeStart
    print(f'Program Time: {programTime}')
