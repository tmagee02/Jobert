import logging
from scraper.company import Company
from playwright.sync_api import Page
from scraper.utils import asyncRandomDelay


logger = logging.getLogger(__name__)


class DiscoveryError(Exception):
    pass


async def asyncRunDiscoveryStrategy(company: Company, page: Page):    
    if not company.urlDiscoveryStrategy:
        logger.debug('%s: No discovery strategy required', company.name)
        return

    logger.debug(
        '%s: %d discovery strategy steps required\n%s',
        company.name, 
        len(company.urlDiscoveryStrategy),
        '\n'.join(
            f"\t{i+1}. {step['type']} --> {step['selector']}" 
            for i, step in enumerate(company.urlDiscoveryStrategy)
            )
    )
    for step in company.urlDiscoveryStrategy:
        await asyncRandomDelay(shortDelay=True)
        await ASYNC_DISCOVERY_ACTIONS[step['type']](step, page)


async def asyncTextInput(step: dict, page: Page):
    inputElement = page.locator(step['selector'])
    count = await inputElement.count()
    if count == 0:
        raise DiscoveryError(f"No inputElement found for selector({step['selector']})")
    if count > 1:
        raise DiscoveryError(f"More than 1 element found for selector({step['selector']}) ({inputElement.count()} found)")
        
    await inputElement.type(step['text'])
    

async def asyncClick(step: dict, page: Page):
    locator = page.locator(step['selector'])
    count = await locator.count()
    if count == 0:
        raise DiscoveryError(f"No element found for selector({step['selector']})")
    if count > 1:
        raise DiscoveryError(f"More than 1 element found for selector({step['selector']}) ({locator.count()} found)")
        
    await locator.click()


async def asyncClickAll(step: dict, page: Page):
    locator = page.locator(step['selector'])
    if not await locator.count(): 
        raise DiscoveryError(f"No elements found for selector({step['selector']})")

    for i in range(await locator.count()):
        element = locator.nth(i)
        await element.click()
        await asyncRandomDelay(shortDelay=True)


ASYNC_DISCOVERY_ACTIONS = {
    'TEXT_INPUT': asyncTextInput,
    'CLICK': asyncClick,
    'CLICK_ALL': asyncClickAll
}
