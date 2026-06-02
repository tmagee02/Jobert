from typing import Tuple, Set
import psycopg2
import json
import pandas as pd
from collections import defaultdict
import time
from scraper.company import Company


def loadExistingDatabaseData() -> Tuple[dict, Set[str]]:
    timeStart = time.perf_counter()
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
            id=row.id, 
            name=row.company_name, 
            baseUrl=row.base_url, 
            searchPath=row.search_path, 
            searchQuery=row.search_query
            )
        companies[row.company_name] = company
    print(dbCompanies)

    df_jobUrls = pd.read_sql_query(qSelectJobUrls, conn)
    dbJobUrls = set(df_jobUrls['job_url'])

    timeEnd = time.perf_counter()
    timeLoadExistingDatabaseData = timeEnd - timeStart
    print(f'\nloadExistingDatabaseData Time: {timeLoadExistingDatabaseData}')
    return (companies, dbJobUrls)


def loadJson(companies: dict) -> Tuple[dict, defaultdict]:
    timeStart = time.perf_counter()
    with open('./scraper/xpathCompany.json', 'r') as file:
        data = json.load(file)

    for company in data:
        companies[company['companyName']].paginationType = company['paginationType'] 
        companies[company['companyName']].urlAttributeType = company['urlAttributeType']
        companies[company['companyName']].xpaths = company['xpaths']
    
    timeEnd = time.perf_counter()
    timeLoadJson = timeEnd - timeStart
    print(f'\nloadJson Time: {timeLoadJson}')