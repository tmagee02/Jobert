import os
import random
import time
import logging
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

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
    load_dotenv()
    email, password = os.getenv('EMAIL_ADDR'), os.getenv('EMAIL_PASS')
    body = f'Scraper run time: {programTime}. See logs attatched.'
    subject = f'Scraper - {timestamp}'
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email
    with open(loggerFile, 'rb') as f:
        fData = f.read()
        msg.add_attachment(fData, maintype='text', subtype='plain', filename='logs.txt')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)
    return

def setupLogging():
    os.makedirs("logs", exist_ok=True)
    os.makedirs('logs/debug', exist_ok=True)
    os.makedirs('logs/jobActivity', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    formatting = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('Jobert Scraper')
    logger.setLevel(logging.DEBUG)
    loggerFile = f'./logs/debug/scraper_logs_{timestamp}.log'
    loggerHandler = logging.FileHandler(loggerFile)
    loggerHandler.setFormatter(formatting)
    logger.addHandler(loggerHandler)
    
    
    jobActivity = logging.getLogger('Job Activity')
    jobActivity.setLevel(logging.INFO)
    jobActivityFile = f'./logs/jobActivity/job_activity_{timestamp}.log'
    jobActivityHandler = logging.FileHandler(jobActivityFile)
    jobActivityHandler.setFormatter(formatting)
    jobActivity.addHandler(jobActivityHandler)

    return logger, jobActivity