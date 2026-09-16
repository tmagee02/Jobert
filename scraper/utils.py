import os
import random
import sys
import time
import logging
import smtplib
import requests
import asyncio
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime
from scraper.job import Job
from functools import wraps
from inspect import iscoroutinefunction


logger = logging.getLogger(__name__)
load_dotenv()
email, password = os.getenv('EMAIL_ADDR'), os.getenv('EMAIL_PASS_MACAIR')


'''
Decorator to time a function
- messagePrefix: What you want the output to say ({message} Time: x.xxxxx)
- loggingLevel: Whether or not this should only be displayed in debug logs only
    True only inserts the time in debug log file
    False inserts in debug log file and stdout
'''
def timed(messagePrefix: str, debugOnly: bool=True):
    timeMessage = '%s Time: %f'
    def decorator(timedFunction: function):
        if iscoroutinefunction(timedFunction):
            @wraps(timedFunction)
            async def asyncWrapper(*args, **kwargs):
                timeStart = time.perf_counter()

                try:
                    return await timedFunction(*args, **kwargs)
                finally:
                    timeEnd = time.perf_counter()
                    totalTime = timeEnd - timeStart
                    if debugOnly:
                        logger.debug(timeMessage, messagePrefix, totalTime)
                    else:
                        logger.info(timeMessage, messagePrefix, totalTime)
            return asyncWrapper
        else:
            @wraps(timedFunction)
            def syncWrapper(*args, **kwargs):
                timeStart = time.perf_counter()

                try:
                    return timedFunction(*args, **kwargs)
                finally:
                    timeEnd = time.perf_counter()
                    totalTime = timeEnd - timeStart
                    if debugOnly:
                        logger.debug(timeMessage, messagePrefix, totalTime)
                    else:
                        logger.info(timeMessage, messagePrefix, totalTime)
            return syncWrapper

    return decorator


async def asyncRandomDelay(shortDelay: bool=False) -> None:
    # global totalDelay
    # logger = logging.getLogger('Jobert Scraper')
    randomTime = random.uniform(0.5, 1.5) if shortDelay else random.uniform(1.5, 5)
    # totalDelay += randomTime
    # logger.debug(f'Random Delay: {randomTime} sec')
    # print(f'Waiting {randomTime} sec.')
    await asyncio.sleep(randomTime)
    return


totalDelay = 0
def randomDelay(shortDelay: bool=False) -> None:
    global totalDelay
    logger = logging.getLogger('Jobert Scraper')
    randomTime = random.uniform(0.5, 1.5) if shortDelay else random.uniform(1.5, 5)
    totalDelay += randomTime
    logger.debug(f'Random Delay: {randomTime} sec')
    time.sleep(randomTime)
    return

def emailLogging(timestamp: str, programTime: float, loggerFile: str):
    body = f'Scraper run time: {programTime}. See logs attatched.'
    subject = f'Scraper - {timestamp}'
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email
    with open(loggerFile.handlers[0].baseFilename, 'rb') as f:
        fData = f.read()
        msg.add_attachment(fData, maintype='text', subtype='plain', filename='logs.txt')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)
    return

def setupLogging():
    os.makedirs('logs/scraper', exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    loggerFile = f'./logs/scraper/scraper_{timestamp}.log'

    fileFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdoutFormatter = logging.Formatter('%(levelname)s (%(name)s)\n%(message)s\n')

    fileHandler = logging.FileHandler(loggerFile, encoding="utf-8")
    fileHandler.setFormatter(fileFormatter)

    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(logging.INFO)
    stdoutHandler.setFormatter(stdoutFormatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(stdoutHandler)


def emailJobsInExperienceRange(jobs: list[Job], minExp: int, maxExp: int):
    jobsInRange = []
    jobsNoExp = []
    for job in jobs:
        if job.minExperience == None and job.maxExperience == None:
            jobsNoExp.append(f'No YOE specified --- ( {job.title} ) found @ {job.url}')
        elif (not job.maxExperience or minExp <= job.maxExperience) and maxExp >= job.minExperience:
            jobsInRange.append(f'Job with desired experience found: [{job.minExperience}, {job.maxExperience}] --- ( {job.title} ) found @ {job.url}')

    if not jobsInRange and not jobsNoExp: 
        return print(f"No jobs found between {minExp} and {maxExp} years of experience")
    
    subject = f'Scraper - Experience [{minExp}, {maxExp}]'
    body = f'Found {len(jobsInRange)} jobs between {minExp} and {maxExp} years of experience. See below: \n\n\n'
    sJobsInRange = '\n'.join(jobsInRange)
    body += sJobsInRange
    body += '\n\n\n---------------Jobs with no specified experience---------------\n\n\n'
    sJobsNoExp = '\n'.join(jobsNoExp)
    body += sJobsNoExp
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)
    return


def sendExperiencePushNotification(jobs: list[Job], experience: int) -> None:
    jobsInRange = []

    for job in jobs:
        if (not job.maxExperience or experience <= job.maxExperience) and job.minExperience and experience >= job.minExperience:
            jobsInRange.append(job)

    if not jobsInRange:
        return

    url = f'https://ntfy.sh/jobert-scraper-{experience}yoe'
    data = f'{len(jobsInRange)} job(s) scraped asking for {experience} year(s) of experience'
    response = requests.post(url, data, timeout=10)
    response.raise_for_status()