from celery_config import celery
from jobs.get_all_users import get_inactive_users
import json
import os
from email.message import EmailMessage
import ssl
import smtplib
from jobs.create_user_report import create_pdf_of_users
from jobs.get_user_email_by_id import get_user_email_by_id


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

def send_activity_report_as_email():
    folder_path = "user_pdfs"
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            user_id = filename.split(".")[0]
            user_email = get_user_email_by_id(user_id) 
            subject = f"Your Activity Report from National Library"
            body = f"Please find your activity report attached."
            attachment_path = os.path.join(folder_path, filename)
            send_email_with_attachment(user_email, subject, body, attachment_path)

def send_email_with_attachment(to_email, subject, body, attachment_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file_path = os.path.join(script_dir, 'secrets.json')

    with open(secrets_file_path) as f:
        secrets = json.load(f)

    sender_email = "palindrajit11@gmail.com"
    password = secrets.get('EMAIL_PASSWORD')
    receiver_email = to_email

    em = EmailMessage()
    em['From'] = "National Library"
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    with open(attachment_path, 'rb') as f:
        attachment_data = f.read()
        attachment_filename = os.path.basename(attachment_path)
        em.add_attachment(attachment_data, maintype='application', subtype='octet-stream', filename=attachment_filename)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.send_message(em)
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

@celery.task
def create_pdf():
    try:
        print("Running create_pdf...")
        create_pdf_of_users()
        send_activity_report_as_email()
        print("Activity Email sent.")
    except Exception as e:
        print(f"Error in create_pdf: {e}")