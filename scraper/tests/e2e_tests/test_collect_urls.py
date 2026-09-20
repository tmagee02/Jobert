import pytest
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import collectAllCompanyJobUrls

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
    ids=lambda c: f'{c.lower()}-collect-urls'
)
async def test_collect_urls(companyName, browser):
    companies, _ = loadExistingDatabaseData()
    loadJson(companies)
    company = {companyName: companies[companyName]}

    jobUrls = await collectAllCompanyJobUrls(browser, company, set())

    assert len(jobUrls) > 0
    for c, url in jobUrls:
        assert c == companyName
        assert isinstance(url, str)
