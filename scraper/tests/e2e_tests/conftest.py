import pytest_asyncio
from playwright.async_api import async_playwright

@pytest_asyncio.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)

        yield browser

        await browser.close()
        