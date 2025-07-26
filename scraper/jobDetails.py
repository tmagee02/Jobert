from playwright.sync_api import Page


def getJobDetails(page: Page, xpaths: dict, companyName: str, jobDetails: dict) -> None:
    # xJobTitle = xpaths[companyName]['jobTitle']
    # xJobDesc = xpaths[companyName]['jobDesc']
    # xLocation = xpaths[companyName]['location']
    # xRemote = xpaths[companyName]['remote']
    # xDatePosted = xpaths[companyName]['datePosted']
    # title = page.locator(xpaths[companyName]['jobTitle'])
    # jobDesc = page.locator(xpaths[companyName]['jobDesc']).evaluate('node => node.outerHTML')
    # location = page.locator(xpaths[companyName]['location'])
    # remote = page.locator(xpaths[companyName]['nextPage']).evaluate('node => node.outerHTML')
    # datePosted = page.locator(xpaths[companyName]['datePosted']).evaluate('node => node.outerHTML')

    # print(title)
    # print(location)



    # soup = BeautifulSoup(html, 'html.parser')
    # jobTitle = soup.find('h1', class_='Copy__title').get_text(strip=True)
    # jobDesc = soup.find('div', class_='RowLayout').get_text(separator=' \n ', strip=True)

    # offices = soup.find('p', string='Office locations')
    # remote = soup.find('p', string='Remote locations')
    # if offices:
    #     offices = offices.find_next_sibling('p').get_text()
    # if remote:
    #     remote = remote.find_next_sibling('p').get_text()

    # jobDetails[jobUrl] = (jobTitle, jobDesc, offices, remote)
    return