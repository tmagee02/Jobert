from playwright.sync_api import Page, expect
import pytest
from typing import Tuple

@pytest.fixture
def jobInfoPage(page: Page):
    page.goto('http://localhost:5173/jobs')

    firstJob = page.locator('//div[@id="jobs"]//a').first
    firstJobText = firstJob.text_content()
    firstJob.click()
    return page, firstJobText


def test_job_info_page_loads(jobInfoPage: Tuple[Page, str]):
    page, jobTitle = jobInfoPage
    expect(page.get_by_role('heading', name=jobTitle)).to_be_visible()


def test_external_link_works(jobInfoPage: Tuple[Page, str]):
    page, _ = jobInfoPage
    link = page.get_by_role('link', name='Apply Now')
    expect(link).to_be_visible()
    url = link.get_attribute('href')

    with page.context.expect_page() as externalPageInfo:
        link.click()

    externalPage = externalPageInfo.value
    expect(externalPage).to_have_url(url)

    