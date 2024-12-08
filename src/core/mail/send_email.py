import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import creds


def send_email(text, meet):

    msg = MIMEMultipart()
    msg['From'] = creds.EMAIL
    msg['To'] = meet.people
    msg['Subject'] = f'Итоги встречи(дата проведения {meet.meet_date})'


    msg.attach(MIMEText(text, 'plain'))

    smtp_server = smtplib.SMTP(creds.SERVER_MAIL, creds.SERVER_PORT)
    smtp_server.starttls()
    smtp_server.login(creds.EMAIL, creds.PASSWORD_MAIL)
    smtp_server.sendmail(creds.EMAIL, meet.people, msg.as_string())
    smtp_server.quit()

