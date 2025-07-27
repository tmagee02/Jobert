import sqlite3
import logging


def writeJobDetailsToFile(jobDetails: dict) -> None:
    count = 1
    with open('./scraper/jobDetails.txt', 'w', encoding='utf-8') as f:
        for jobUrl, (title, jobDesc, offices, remote, datePosted, idCompany) in jobDetails.items():
            f.write(f'{count}. {jobUrl}')
            count += 1
            f.write(f'\n{title}\n')
            if offices:
                strOffice = '; '.join(offices)
                f.write(f'Office Locations: {strOffice}\n')
            if remote:
                f.write(f'Remote Locations: {remote}\n')
            if datePosted:
                f.write(f'Date Posted: {datePosted}\n')
            f.write(f'\n{jobDesc}\n')
            f.write('\n\n--------------------\n--------------------\n--------------------\n\n')
    return


def insertJobToDatabase(jobDetails: dict) -> None:
    logger = logging.getLogger('Jobert Scraper')
    with sqlite3.connect('./db/jobert.db') as conn:
        cursor = conn.cursor()
        for jobUrl, (title, jobDesc, offices, remote, datePosted, idCompany) in jobDetails.items():
            qInsertJob = '''
                insert into Job (job_url, title, job_desc, company_id)
                values (?, ?, ?, ?)
                '''
            try:
                cursor.execute(qInsertJob, (jobUrl, title, jobDesc, idCompany))
                logger.info(f'Inserting row into db for Job: {title}. Good.')
                idJob = cursor.lastrowid
            except sqlite3.IntegrityError:
                logger.info(f'Row in db for Job: {title} already exists. Skipping.')
    return