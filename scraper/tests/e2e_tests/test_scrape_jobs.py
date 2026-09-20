import pytest
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import collectAllCompanyJobUrls
from scraper.scrapeJobs import scrapeAllJobs

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'companyName', [
        'Stripe',
        'Airbnb',
        'Block',
        'Databricks',
        'OpenAI',
        'Uber',
        'Apple',
        'Plaid',
        'Brex',
        'Spotify',
        'Google',
        'Anthropic',
        'Datadog',
        'NVIDIA'
    ],
    ids=lambda c: f'{c.lower()}-scrape-jobs'
)
async def test_scrape_jobs(companyName, browser):
    companies, _ = loadExistingDatabaseData()
    loadJson(companies)
    company = {companyName: companies[companyName]}

    jobUrls = await collectAllCompanyJobUrls(browser, company, set())
    jobsScraped = await scrapeAllJobs(browser, company, jobUrls)

    for job in jobsScraped:
        assert job.idCompany == company[companyName].id
        assert len(job.title) > 0
        assert len(job.jobDesc) > 0
