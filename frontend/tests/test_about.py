from playwright.sync_api import Page, expect
import pytest

@pytest.fixture
def aboutPage(page: Page):
    page.goto('http://localhost:5173/about')
    return page


def test_about_page_loads(aboutPage: Page):
    expect(aboutPage).to_have_title('About')
    expect(aboutPage.get_by_role('heading', name='About')).to_be_visible()

    