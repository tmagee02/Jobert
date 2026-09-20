import pytest
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import asyncCollectAllCompanyJobUrls

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
    ids=lambda c: f'{c.lower()}-urls-live'
)
async def test_extract_urls(companyName, browser):
    companies, _ = loadExistingDatabaseData()
    loadJson(companies)
    company = {companyName: companies[companyName]}

    jobUrls = await asyncCollectAllCompanyJobUrls(browser, company, set())

    assert len(jobUrls) > 0
    for c, url in jobUrls:
        assert c == companyName
        assert isinstance(url, str)
