from playwright.sync_api import Page, expect
import pytest

@pytest.fixture
def jobsPage(page: Page):
    page.goto('http://localhost:5173/jobs')
    return page


def test_jobs_page_loads(jobsPage: Page):
    expect(jobsPage).to_have_title('Jobs')
    expect(jobsPage.get_by_role('heading', name='Jobs', exact=True)).to_be_visible()



def test_job_link_works(jobsPage: Page):
    firstJob = jobsPage.locator('//li').first
    firstJobText = firstJob.text_content()
    firstJob.click()

    expect(jobsPage.get_by_role('heading', name=firstJobText)).to_be_visible()
    # link = jobsPage.get_by_role('link', name='Apply Now').first
    # expect(link).to_be_visible()
    # url = link.get_attribute('href')
    # print(url)

    # with jobsPage.context.expect_page() as externalPageInfo:
    #     link.click()

    # externalPage = externalPageInfo.value
    # expect(externalPage).to_have_url(url)