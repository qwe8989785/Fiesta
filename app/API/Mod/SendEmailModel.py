# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 18:43:45 2020

@author: user
"""

import smtplib
from email.mime.text import MIMEText

def ConfirmSend(to, template):
    gmail_user = 'FiestaConfirmMail@gmail.com'
    gmail_password = 'Skills39' # your gmail password
    msg = MIMEText(template,'html','utf-8')
    msg['Subject'] = "Please confirm your email"
    msg['From'] = gmail_user
    msg['To'] = to
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()
