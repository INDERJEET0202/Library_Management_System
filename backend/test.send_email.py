import json
import os
from email.message import EmailMessage
import ssl
import smtplib


def send_email(to_email, subject, body):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file_path = os.path.join(script_dir, 'secrets.json')

    with open(secrets_file_path) as f:
        secrets = json.load(f)

    sender_email = "senderemail@gmail.com"
    password = secrets.get('EMAIL_PASSWORD')
    receiver_email = to_email

    subject = subject
    body = body


    em = EmailMessage()
    em['From'] = "National Library"
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, em.as_string())
        print("Email sent successfully.")


send_email("receiveremail@gmail.com", "You have been inactive", "Please visit our site to keep your account active.")