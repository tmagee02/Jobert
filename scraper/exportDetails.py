import sqlite3
import logging
import time


def writeJobDetailsToFile(jobDetails: dict) -> None:
    timeStart = time.perf_counter()
    count = 1

    with open('./scraper/jobDetails.txt', 'w', encoding='utf-8') as f:
        for jobUrl, (title, jobDesc, offices, remote, datePosted, idCompany) in jobDetails.items():
            f.write(f'{count}. {jobUrl}')
            count += 1
            f.write(f'\n{title}\n')
            if offices:
                print(offices, str(type(offices)))
                # strOffice = '; '.join(offices)
                # print(str(type(strOffice)))
                f.write(f'Office Locations: {offices}\n')
            if remote:
                print(remote, str(type(remote)))
                f.write(f'Remote Locations: {remote}\n')
            if datePosted:
                f.write(f'Date Posted: {datePosted}\n')
            f.write(f'\n{jobDesc}\n')
            f.write('\n\n--------------------\n--------------------\n--------------------\n\n')

    timeEnd = time.perf_counter()
    timeWriteJobDetailsToFile= timeEnd - timeStart
    print(f'\nwriteJobDetailsToFile Time: {timeWriteJobDetailsToFile}\n')
    return


def insertJobsToDatabase(jobDetails: dict) -> None:
    timeStart = time.perf_counter()
    logger = logging.getLogger('Jobert Scraper')
    logger.info('Inserting jobs into database')
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

    timeEnd = time.perf_counter()
    timeInsertJobsToDatabase = timeEnd - timeStart
    print(f'\ninsertJobsToDatabase Time: {timeInsertJobsToDatabase}\n')
    return