import pytest
from playwright.sync_api import sync_playwright
from scraper.discoveryStrategy import textInput, click, clickAll


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        page.goto('https://www.anthropic.com/careers/jobs')
        yield page

        browser.close()


def test_text_input(page):
    step = {
        'type': 'TEXT_INPUT',
        'selector': '//input[@placeholder="Search roles"]',
        'text': 'testing textInput()'
    }

    textInput(step, page)
    inputElement = page.locator(step['selector'])

    assert inputElement.input_value() == step['text']



def test_click(page):
    step = {
        'type': 'CLICK',
        'selector': '//section/div[position() > 1][1]'
    }

    checkbox = page.locator('#team-0')
    assert not checkbox.is_checked()
    click(step, page)
    assert checkbox.is_checked()


def test_click_all(page):
    step = {
        'type': 'CLICK_ALL',
        'selector': '//section/div[position() > 1]',
    }

    checkboxes = page.locator('//input[contains(@id, "team")]')
    for i in range(checkboxes.count()):
        assert not checkboxes.nth(i).is_checked()

    clickAll(step, page)

    for i in range(checkboxes.count()):
        assert checkboxes.nth(i).is_checked()
