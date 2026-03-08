from scraper.dataLoader import loadJson, loadExistingDatabaseData
from pandas import DataFrame
from collections import defaultdict

def test_load_json():
    urlRenderTypes, xpaths = loadJson()
    possibleRenderTypes = {'Next Page', 'Show More', None}
    requiredKeys = {'jobUrl', 'jobTitle', 'jobDesc', 'location'}

    assert isinstance(urlRenderTypes, dict)
    assert all(renderType in possibleRenderTypes for renderType in urlRenderTypes.values())

    assert isinstance(xpaths, defaultdict)
    for company, xpath in xpaths.items():
        assert isinstance(company, str)
        assert isinstance(xpath, dict)
        for key in requiredKeys:       #all values that NEED a value
            assert key in xpath, f'{key} should exist in each xpath'
            assert xpath[key], f'{key} should have a value'

def test_db_query():
    dbCompanies, dbJobUrls = loadExistingDatabaseData()

    assert isinstance(dbCompanies, DataFrame)
    assert not dbCompanies.empty

    assert isinstance(dbJobUrls, set)
    assert all(isinstance(url, str) for url in dbJobUrls)