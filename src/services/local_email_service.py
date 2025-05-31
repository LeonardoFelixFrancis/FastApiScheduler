from src.interfaces.email.email_interface import IEmailService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

class LocalEmailService(IEmailService):

    def send(self, to, subject, template, fields):
        with open(f'assets/mail_templates/{template}', 'r',  encoding='utf-8') as template_file:
            template_contents = template_file.read()
            logging.info(template_contents)
            template_contents = template_contents.format(**fields)

            smtp_server = os.getenv('SMTP_SERVER')
            port = int(os.getenv('MAIL_PORT'))
            password = os.getenv('MAIL_PASSWORD')
            sender = os.getenv('SENDER_MAIL')

            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = sender
            message['To'] = to

            message.attach(MIMEText(template_contents, 'html', 'utf-8'))

            try:
                with smtplib.SMTP_SSL(smtp_server, port) as mail_server:
                    mail_server.login(sender, password)
                    mail_server.sendmail(sender, to, message.as_string())
                
            except Exception as e:
                print(f'Erro ao enviar o email: {e}')