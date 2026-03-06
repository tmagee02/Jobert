from playwright.sync_api import Page, expect
import re
import pytest


@pytest.fixture
def homepage(page: Page):
    page.goto("http://localhost:5173/")
    return page


def test_homepage_loads(homepage: Page):

    expect(homepage).to_have_title("Homepage")
    expect(homepage.get_by_role('heading', name='Home')).to_be_visible()


@pytest.mark.parametrize(
    'linkName', [
        'Jobs',
        'Watchlist',
        'About'
    ]
)
def test_links_work(homepage: Page, linkName: str):
    link = homepage.get_by_role('link', name=linkName)
    expect(link).to_be_visible()

    link.click()
    expect(homepage).to_have_title(linkName)
    