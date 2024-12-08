import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import creds


def get_message_for_users(meet):
    """Отправка сообщений пользователям"""

    msg = MIMEMultipart()
    msg['From'] = creds.EMAIL
    msg['To'] = meet.organizer
    msg['Subject'] =  'Потверждение встречи'


    text = (f'Встреча была принята на {meet.meet_date}'
            f'Сылка на видиовстречу: {meet.room_uri}')


    msg.attach(MIMEText(text, 'plain'))

    smtp_server = smtplib.SMTP(creds.SERVER_MAIL, creds.SERVER_PORT)
    smtp_server.starttls()
    smtp_server.login(creds.EMAIL, creds.PASSWORD_MAIL)
    smtp_server.sendmail(creds.EMAIL, meet.organizer, msg.as_string())
    smtp_server.quit()

