import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from scraper.discoveryStrategy import textInput, click, clickAll


@pytest_asyncio.fixture
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        await page.goto('https://www.anthropic.com/careers/jobs')
        yield page

        await browser.close()


@pytest.mark.asyncio
async def test_text_input(page):
    step = {
        'type': 'TEXT_INPUT',
        'selector': '//input[@placeholder="Search roles"]',
        'text': 'testing textInput()'
    }

    await textInput(step, page)
    inputElement = page.locator(step['selector'])

    assert await inputElement.input_value() == step['text']


@pytest.mark.asyncio
async def test_click(page):
    step = {
        'type': 'CLICK',
        'selector': '//section/div[position() > 1][1]'
    }

    checkbox = page.locator('#team-0')
    assert not await checkbox.is_checked()
    await click(step, page)
    assert await checkbox.is_checked()


@pytest.mark.asyncio
async def test_click_all(page):
    step = {
        'type': 'CLICK_ALL',
        'selector': '//section/div[position() > 1]',
    }

    checkboxes = page.locator('//input[contains(@id, "team")]')
    for i in range(await checkboxes.count()):
        assert not await checkboxes.nth(i).is_checked()

    await clickAll(step, page)

    for i in range(await checkboxes.count()):
        assert await checkboxes.nth(i).is_checked()
