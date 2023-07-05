import requests
from bs4 import BeautifulSoup
import os
from dotenv import dotenv_values
config = dotenv_values(".env")

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

now = datetime.datetime.now

content = ''


def extract_news(url):
    print('Extracting hacker news stories...')
    cnt = ''
    cnt += ('<b>HN Top stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):
        cnt +=((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
    return (cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of message')

print('Composing email...')

SERVER='smtp.gmail.com'
PORT=587
FROM=config['EMAIL_SENDER']
TO=config['EMAIL_RECIEVER']
PASS=config['EMAIL_PASS']

msg = MIMEMultipart()

msg['Subject'] = 'TOP NEWS' 
msg['From'] = FROM
msg['To']=TO

msg.attach(MIMEText(content, 'html'))

print('Initiating server')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent..')
server.quit()



