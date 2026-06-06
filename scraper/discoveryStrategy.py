from scraper.company import Company
from playwright.sync_api import Page
from scraper.utils import randomDelay

class DiscoveryError(Exception):
    pass


def runDiscoveryStrategy(company: Company, page: Page):
    if not company.urlDiscoveryStrategy:
        return print(f'{company.name}: No discovery strategy required')

    print(f'{company.name}: {len(company.urlDiscoveryStrategy)} discovery strategy steps required')
    for i, step in enumerate(company.urlDiscoveryStrategy):
        print(f"\t{i+1}. {step['type']} --> {step['selector']}")
        randomDelay()
        DISCOVERY_ACTIONS[step['type']](step, page)


def textInput(step: dict, page: Page):
    inputElement = page.locator(step['selector'])
    count = inputElement.count()
    if count == 0:
        raise DiscoveryError(f"No inputElement found for selector({step['selector']})")
    if count > 1:
        raise DiscoveryError(f"More than 1 element found for selector({step['selector']}) ({inputElement.count()} found)")
        
    inputElement.type(step['text'])
    

def click(step: dict, page: Page):
    locator = page.locator(step['selector'])
    count = locator.count()
    if count == 0:
        raise DiscoveryError(f"No element found for selector({step['selector']})")
    if count > 1:
        raise DiscoveryError(f"More than 1 element found for selector({step['selector']}) ({locator.count()} found)")
        
    locator.click()


def clickAll(step: dict, page: Page):
    locator = page.locator(step['selector'])
    if not locator.count(): 
        raise DiscoveryError(f"No elements found for selector({step['selector']})")

    for i in range(locator.count()):
        element = locator.nth(i)
        element.click()
        randomDelay(shortDelay=True)


DISCOVERY_ACTIONS = {
    'TEXT_INPUT': textInput,
    'CLICK': click,
    'CLICK_ALL': clickAll
}
