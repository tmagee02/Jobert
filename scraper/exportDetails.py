import psycopg2
import logging
from scraper.job import Job
from scraper.utils import timed

logger = logging.getLogger(__name__)

@timed('writeJobDetailsToFile')
def writeJobDetailsToFile(jobs: list[Job]) -> None:
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


@timed('insertJobsToDatabase')
def insertJobsToDatabase(jobs: list[Job]) -> None:
    conn = psycopg2.connect(
        host='localhost',
        port=5333,
        database='jobert_db',
        user='timmagee',
        password='password'
    )
    cursor = conn.cursor()
    qInsertJob = '''
        insert into job (job_url, title, job_desc, company_id, min_salary, max_salary, min_experience, max_experience)
        values (%s, %s, %s, %s, %s, %s, %s, %s)
        '''

    for job in jobs:
        try:
            jobVals = (job.url, job.title, job.jobDesc, job.idCompany, job.minSalary, job.maxSalary, job.minExperience, job.maxExperience)
            cursor.execute(qInsertJob, jobVals)
            logger.debug(f'Inserted job: {job.title}')
        except Exception as e:
            logger.warning(f'Failed inserting {job.title}: {e}')
    
    conn.commit()
    cursor.close()
    conn.close()