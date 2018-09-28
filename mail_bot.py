# -*- coding: utf-8 -*-
#Spam-bot 
#(c) baxatob, 2017

import smtplib
import random
import time
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

MAIL_COUNT = int(input("Please input the number of emails: "))
SERVER =  'define.mail.server'

SEND_FROM = ['vladimir.putin@kremlin.ru']
SEND_TO = ['define@mail.list.here']


def send_mail(send_from, send_to, subject, text, server, files):
	
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
	
	
if __name__ == '__main__':
	os.system('cls')
	print('SPAM BOT STARTED...\n')
	time.sleep(3)
	
	counter = {name : 0 for name in SEND_FROM}
	
	for id_ in range(1, MAIL_COUNT+1):
		server = SERVER
		send_from = random.choice(SEND_FROM)
		counter[send_from] += 1
		send_to = SEND_TO
		subject = 'TEST SERVICE CALL #{}'.format(id_)
		text = 'bla{0}-bla{0}-bla{0}\n'.format(id_) *10
		if not id_%10:
			files = ['attachment.txt']
		else: files = None
		
		print('Sending email #{}...'.format(id_))
		send_mail(send_from, send_to, subject, text, server, files)
		time.sleep(1)
		
	print('\n\nTOTAL SENT:\n')
	for name in SEND_FROM:
		print('{} ..... {} mails'.format(name, counter[name]))
