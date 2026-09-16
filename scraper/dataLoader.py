from typing import Tuple, Set
import psycopg2
import json
import pandas as pd
from collections import defaultdict
from scraper.utils import timed
from scraper.company import Company


NEED_TO_FIX = {'Uber'}
WHITELIST = {}

@timed('loadExistingDatabaseData')
def loadExistingDatabaseData() -> Tuple[dict, Set[str]]:
    qSelectCompany = '''
        select * 
        from Company
        '''
    qSelectJobUrls = '''
        select job_url
        from Job
        '''

    conn = psycopg2.connect(
        host='localhost',
        port='5333',
        database='jobert_db',
        user='timmagee',
        password='password'
    )
    companies = {}
    dbCompanies = pd.read_sql_query(qSelectCompany, conn)
    for row in dbCompanies.itertuples():
        company = Company(
            id=row.company_id, 
            name=row.company_name, 
            baseUrl=row.base_url, 
            searchPath=row.search_path, 
            searchQuery=row.search_query
            )
        if ((WHITELIST and row.company_name in WHITELIST) or 
            (not WHITELIST and row.company_name not in NEED_TO_FIX)):
            companies[row.company_name] = company
    print(dbCompanies)

    df_jobUrls = pd.read_sql_query(qSelectJobUrls, conn)
    dbJobUrls = set(df_jobUrls['job_url'])

    return (companies, dbJobUrls)


@timed('loadJson')
def loadJson(companies: dict) -> Tuple[dict, defaultdict]:
    with open('./scraper/xpathCompany.json', 'r') as file:
        data = json.load(file)

    for company in data:
        companyName = company['companyName']
        if (WHITELIST and companyName not in WHITELIST) or companyName in NEED_TO_FIX:
            continue

        c = companies[company['companyName']]
        c.urlDiscoveryStrategy = company['urlDiscoveryStrategy']
        c.paginationType = company['paginationType'] 
        c.urlAttributeType = company['urlAttributeType']
        c.xpaths = company['xpaths']