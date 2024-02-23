from celery_config import celery
from get_all_users import get_inactive_users
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

    sender_email = "palindrajit11@gmail.com"
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


@celery.task
def send_remainder():
    try:
        print("Running my_task...")
        users = get_inactive_users()
        print(users[0][1])
        for user in users:
            print(f"Sending email to {user[1]}")
            send_email(user[1], "You have been inactive", "Please visit our site to keep your account active.")


        print("Task completed.")
    except Exception as e:
        print(f"Error in my_task: {e}")