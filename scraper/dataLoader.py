import sqlite3
import json
import pandas as pd
from collections import defaultdict

def loadExistingDatabaseData():
        qSelectCompany = '''
            select * 
            from Company
            '''
        qSelectJobUrls = '''
            select job_url
            from Job
            '''

        with sqlite3.connect('./db/jobert.db') as conn:
            dbCompanies = pd.read_sql_query(qSelectCompany, conn)
            print(dbCompanies)
            df_jobUrls = pd.read_sql_query(qSelectJobUrls, conn)
        
        dbJobUrls = set(df_jobUrls['job_url'])
        return dbCompanies, dbJobUrls


def loadJson():
    with open('./scraper/xpathCompany.json', 'r') as file:
        data = json.load(file)

    urlRenderTypes = {}
    xpaths = defaultdict(dict)
    for company in data:
        urlRenderTypes[company['companyName']] = company['urlRenderType']
        xpaths[company['companyName']] = company['xpaths']
    return urlRenderTypes, xpaths