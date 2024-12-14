import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path="./.env")

# Constants
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
COMPOSITE_USER_URL = os.getenv("COMPOSITE_USER_URL")
COMPOSITE_UPCOMING_REMINDER_URL = os.getenv("COMPOSITE_UPCOMING_REMINDER_URL")


def send_email(to_email, subject, body):
    """
    Send an email using SMTP.
    """
    try:
        # Create email content
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = MAIL_USERNAME
        msg["To"] = to_email

        # Connect to the SMTP server
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            if MAIL_USE_TLS:
                server.starttls()  # Upgrade the connection to secure
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def fetch_reminders_and_notify():
    """
    Fetch reminders grouped by user from the microservice and send emails.
    """
    try:
        response = requests.get(COMPOSITE_UPCOMING_REMINDER_URL)
        response.raise_for_status()  
        reminders = response.json()["reminders"]
        #print(f"Fetched reminders: {reminders}")

        for reminder_group in reminders:
            user_id = reminder_group["user_id"]
            tasks = reminder_group["tasks"]

            # Assuming COMPOSITE_USER_URL is a base URL like "http://example.com/users/"
            url = f"{COMPOSITE_USER_URL}/{user_id}" if not COMPOSITE_USER_URL.endswith('/') else f"{COMPOSITE_USER_URL}{user_id}"
            user_instance = requests.get(url)
            to_email = user_instance.json()["email"]
            #print("to_email", to_email, "user_id", user_id)

            subject = "Your Upcoming Reminders"
            body = "Here are your tasks due soon:\n\n"
            for task in tasks:
                body += f"- Task ID: {task['task_id']}, Due: {task['reminder_time']}, Message: {task['message']}\n"

            send_email(to_email, subject, body)

    except Exception as e:
        print(f"Failed to fetch reminders or send emails: {e}")


def lambda_handler(event, context):
    fetch_reminders_and_notify()
    return {
        "statusCode": 200,
        "body": "Reminders processed and emails sent successfully!"
    }

if __name__ == "__main__":
    fetch_reminders_and_notify()
