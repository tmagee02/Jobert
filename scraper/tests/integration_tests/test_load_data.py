from scraper.company import Company
from scraper.dataLoader import loadJson, loadExistingDatabaseData
from collections import defaultdict

def test_load_json():
    companies, _ = loadExistingDatabaseData()
    loadJson(companies)
    possiblePaginationTypes = {'Next Page', 'Show More', None}
    possibleUrlAttributeTypes = {'href', 'data-info'}
    requiredKeys = {'jobUrl', 'jobTitle', 'jobDesc', 'location'}

    assert all(company.paginationType in possiblePaginationTypes for company in companies.values())
    assert all(company.urlAttributeType in possibleUrlAttributeTypes for company in companies.values())

    assert all(isinstance(company.xpaths, dict) for company in companies.values())
    for company in companies.values():
        for key in requiredKeys:       #all values that NEED a value
            assert key in company.xpaths, f'{key} should exist in each xpath'
            assert company.xpaths[key], f'{key} should have a value'

def test_db_query():
    companies, dbJobUrls = loadExistingDatabaseData()

    assert isinstance(companies, dict)
    assert all(isinstance(companyName, str) for companyName in companies)
    assert all(isinstance(company, Company) for company in companies.values())

    assert isinstance(dbJobUrls, set)
    assert all(isinstance(url, str) for url in dbJobUrls)