import pytest
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import getAllJobUrls

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
        'Google'
    ],
    ids=lambda c: f'{c.lower()}-urls-live'
)
def test_extract_urls(companyName, page):
    companies, _ = loadExistingDatabaseData()
    loadJson(companies)
    company = {companyName: companies[companyName]}

    jobUrls = getAllJobUrls(company, page)

    assert len(jobUrls) > 0
    for c, url in jobUrls:
        assert c == companyName
        assert isinstance(url, str)