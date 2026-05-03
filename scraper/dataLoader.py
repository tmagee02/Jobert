from typing import Tuple, Set
import psycopg2
import json
import pandas as pd
from pandas import DataFrame
from collections import defaultdict
import time


def loadExistingDatabaseData() -> Tuple[DataFrame, Set[str]]:
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
    dbCompanies = pd.read_sql_query(qSelectCompany, conn)
    print(dbCompanies)
    df_jobUrls = pd.read_sql_query(qSelectJobUrls, conn)
    
    dbJobUrls = set(df_jobUrls['job_url'])

    timeEnd = time.perf_counter()
    timeLoadExistingDatabaseData = timeEnd - timeStart
    print(f'\nloadExistingDatabaseData Time: {timeLoadExistingDatabaseData}')
    return (dbCompanies, dbJobUrls)


def loadJson() -> Tuple[dict, defaultdict]:
    timeStart = time.perf_counter()
    with open('./scraper/xpathCompany.json', 'r') as file:
        data = json.load(file)

    urlRenderTypes = {}
    xpaths = defaultdict(dict)
    for company in data:
        urlRenderTypes[company['companyName']] = company['urlRenderType']
        xpaths[company['companyName']] = company['xpaths']
    
    timeEnd = time.perf_counter()
    timeLoadJson = timeEnd - timeStart
    print(f'\nloadJson Time: {timeLoadJson}')
    return urlRenderTypes, xpaths