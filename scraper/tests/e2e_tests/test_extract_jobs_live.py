import pytest
from scraper.dataLoader import loadExistingDatabaseData, loadJson
from scraper.jobUrls import collectAllCompanyJobUrls
from scraper.jobDetails import getAllJobDetails

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

    jobUrls = collectAllCompanyJobUrls(company, page)
    jobDetails = getAllJobDetails(set(), page, jobUrls, company)

    for url, job in jobDetails.items():
        assert job.url == url
        assert job.idCompany == company[companyName].id
        assert len(job.title) > 0
        assert len(job.jobDesc) > 0