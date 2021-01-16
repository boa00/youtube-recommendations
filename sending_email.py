import smtplib
import secrets
from datetime import datetime

EMAIL_ADRESS = secrets.EMAIL_ADRESS
EMAIL_PASSWORD = secrets.EMAIL_PASSWORD 

def send_email(body):

  with smtplib.SMTP('smtp.gmail.com', port=587) as smtp:
    smtp.starttls()
    smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

    # create title for the email message
    today = datetime.today().strftime('%d-%m-%Y')
    subject = f'YouTube Recommendations: {today}'

    message = f'Subject: {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADRESS, EMAIL_ADRESS, message)

