import sqlite3
import logging
import time
from scraper.job import Job


def writeJobDetailsToFile(jobs: list[Job]) -> None:
    timeStart = time.perf_counter()
    count = 1

    with open('./scraper/jobDetails.txt', 'w', encoding='utf-8') as f:
        for job in jobs:
            f.write(f'{count}. {job.url}')
            count += 1
            f.write(f'\n{job.title}\n')
            f.write(f'Office Locations: {str(job.offices)}\n')
            f.write(f'Remote Locations: {str(job.remote)}\n')
            f.write(f'Date Posted: {str(job.datePosted)}\n')
            f.write(f'\n{job.jobDesc}\n')
            f.write('\n\n--------------------\n--------------------\n--------------------\n\n')

    timeEnd = time.perf_counter()
    timeWriteJobDetailsToFile= timeEnd - timeStart
    print(f'\nwriteJobDetailsToFile Time: {timeWriteJobDetailsToFile}\n')
    return


def insertJobsToDatabase(jobs: list[Job]) -> None:
    timeStart = time.perf_counter()
    logger = logging.getLogger('Jobert Scraper')
    logger.info('Inserting jobs into database')
    with sqlite3.connect('./db/jobert.db') as conn:
        cursor = conn.cursor()
        for job in jobs:
            qInsertJob = '''
                insert into Job (job_url, title, job_desc, company_id, min_salary, max_salary, min_experience, max_experience)
                values (?, ?, ?, ?, ?, ?, ?, ?)
                '''
            try:
                jobVals = (job.url, job.title, job.jobDesc, job.idCompany, job.minSalary, job.maxSalary, job.minExperience, job.maxExperience)
                cursor.execute(qInsertJob, jobVals)
                logger.info(f'Inserting row into db for Job: {job.title}. Good.')
                idJob = cursor.lastrowid
            except sqlite3.IntegrityError:
                logger.info(f'Row in db for Job: {job.title} already exists. Skipping.')

    timeEnd = time.perf_counter()
    timeInsertJobsToDatabase = timeEnd - timeStart
    print(f'\ninsertJobsToDatabase Time: {timeInsertJobsToDatabase}\n')
    return