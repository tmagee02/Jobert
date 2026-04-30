from typing import Tuple, Set
import psycopg2
import json
import pandas as pd
from pandas import DataFrame
from collections import defaultdict


def loadExistingDatabaseData() -> Tuple[DataFrame, Set[str]]:
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
    return (dbCompanies, dbJobUrls)


def loadJson() -> Tuple[dict, defaultdict]:
    with open('./scraper/xpathCompany.json', 'r') as file:
        data = json.load(file)

    urlRenderTypes = {}
    xpaths = defaultdict(dict)
    for company in data:
        urlRenderTypes[company['companyName']] = company['urlRenderType']
        xpaths[company['companyName']] = company['xpaths']
    return urlRenderTypes, xpaths