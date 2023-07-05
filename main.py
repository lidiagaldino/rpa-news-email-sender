import requests
from bs4 import BeautifulSoup
import os
from dotenv import dotenv_values
config = dotenv_values(".env")

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class NewsEmailSender:
    def __init__(self):
        self.sender = config['EMAIL_SENDER']
        self.reciever = config['EMAIL_RECIEVER']
        self.password = config['EMAIL_PASS']
        self.url = config['URL']
        self.content = ''
        self.cnt = ''
        self.msg = MIMEMultipart()
    
    def extract_news(self):
        print('Extracting hacker news stories...')
        self.cnt += ('<b>HN Top stories:</b>\n'+'<br>'+'-'*50+'<br>')
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):
            self.cnt +=((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
        self.content += self.cnt
        self.content += ('<br>------<br>')
        self.content += ('<br><br>End of message')
    
    def prepare_email(self):
        self.msg['Subject'] = 'TOP NEWS' 
        self.msg['From'] = self.sender
        self.msg['To']=self.reciever
        self.msg.attach(MIMEText(self.content, 'html'))

    def send_email(self):
        server = smtplib.SMTP(config['SERVER'], config['PORT'])
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.reciever, self.msg.as_string())
        server.quit()
    
    def run(self):
        self.extract_news()
        self.prepare_email()
        self.send_email()

bot = NewsEmailSender()
bot.run()





