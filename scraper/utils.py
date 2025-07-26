import os
import random
import time
import logging
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


def randomDelay(shortDelay: bool=False) -> None:
    logger = logging.getLogger('Jobert Scraper')
    randomTime = random.uniform(0.5, 1.5) if shortDelay else random.uniform(1.5, 5)
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