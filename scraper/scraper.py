import requests
from bs4 import BeautifulSoup


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
    
    jobUrls = getJobUrls(baseUrl, path, query)
    print(len(jobUrls), jobUrls)
    return


def getJobUrls(baseUrl: str, path: str, query: str) -> list[str]:
    searchUrl = baseUrl + path + query
    response = requests.get(searchUrl)
    print(str(response.status_code))
    if response.status_code != 200:
        return
    
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    jobs = soup.find_all("a", class_="Link JobsListings__link")
    jobUrls = []

    for i, job in enumerate(jobs):
        jobUrl = baseUrl + job.get("href")
        jobUrls.append(jobUrl)
    
    return jobUrls


'''
before getting job details, i should learn about response vs session
'''
def getJobDetails():
    return





    
if __name__ == "__main__":
    print(".\n.\n.\n.\n.\n")
    main()
