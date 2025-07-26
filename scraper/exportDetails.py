import sqlite3
import logging


def writeJobDetailsToFile(jobDetails: dict) -> None:
    with open('./scraper/jobDetails.txt', 'w') as f:
        for jobUrl, (title, jobDesc, offices, remote) in jobDetails.items():
            f.write(jobUrl)
            f.write(f'\n{title}\n')
            if offices:
                f.write(f'Office Locations: {offices}\n')
            if remote:
                f.write(f'Remote Locations: {remote}\n')
            f.write('\n')
            f.write(jobDesc)
            f.write('\n\n--------------------\n--------------------\n--------------------\n\n')
    return


def insertJobToDatabase(jobDetails: dict, idCompany: int) -> None:
    logger = logging.getLogger('Jobert Scraper')
    with sqlite3.connect('./db/jobert.db') as conn:
        cursor = conn.cursor()
        for jobUrl, (title, jobDesc, offices, remote) in jobDetails.items():
            insertJob = '''
                insert into Job (job_url, title, job_desc, company_id)
                values (?, ?, ?, ?)
                '''
            try:
                cursor.execute(insertJob, (jobUrl, title, jobDesc, idCompany))
                logger.info(f'Inserting row into db for Job: {title}. Good.')
                idJob = cursor.lastrowid
            except sqlite3.IntegrityError:
                logger.info(f'Row in db for Job: {title} already exists. Skipping.')
    return