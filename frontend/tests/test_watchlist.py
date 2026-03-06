from playwright.sync_api import Page, expect
import pytest


@pytest.fixture
def watchlistPage(page: Page):
    page.goto('http://localhost:5173/watchlist')
    return page


def test_watchlist_page_loads(watchlistPage: Page):
    expect(watchlistPage).to_have_title('Watchlist')
    expect(watchlistPage.get_by_role('heading', name='Watchlist')).to_be_visible()