import smtplib
from email.mime.text import MIMEText
import json
import schedule
import time
import sqlite3
from datetime import datetime, timedelta
import os

# Define the database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "shifts.db")

# Load configuration
with open(os.path.join(BASE_DIR, "config", "config.json"), "r") as f:
    config = json.load(f)

SENDER_EMAIL = config["email"]["sender"]
SENDER_PASSWORD = config["email"]["password"]
RECEIVER_EMAIL = config["email"]["receiver"]
SMTP_SERVER = config["email"]["smtp_server"]
SMTP_PORT = config["email"]["smtp_port"]

def get_next_week_availability():
    """Query the database for availability for the next week (Sunday to Saturday)."""
    today = datetime.now()
    days_until_sunday = (6 - today.weekday() + 7) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    start_date = today + timedelta(days=days_until_sunday)
    end_date = start_date + timedelta(days=6)

    # Convert to YYYY-MM-DD for SQLite comparison
    start_date_sql = start_date.strftime("%Y-%m-%d")
    end_date_sql = end_date.strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Convert stored DD-MM-YYYY to YYYY-MM-DD for comparison
    cursor.execute("""
        SELECT date, start_time, end_time 
        FROM shifts 
        WHERE (substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2))
              BETWEEN ? AND ? 
        AND status = 'pending'
    """, (start_date_sql, end_date_sql))
    shifts = cursor.fetchall()
    conn.close()

    if not shifts:
        return ["No availability submitted for this week."]
    availability = []
    for shift in shifts:
        date, start_time, end_time = shift
        availability.append(f"- {date}: {start_time} - {end_time}")
    return availability

def send_weekly_email():
    """Send an email with the next week's availability."""
    availability = get_next_week_availability()
    body = "Here’s my availability for the upcoming week:\n" + "\n".join(availability)
    # Use DD-MM-YYYY for the email subject
    subject = f"Availability for Week of {datetime.now().strftime('%d-%m-%Y')}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully at {datetime.now()}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule the email to send every Thursday at 9:00 AM
schedule.every().thursday.at("09:00").do(send_weekly_email)

# Test the function immediately (remove this in production)
send_weekly_email()

# Keep the script running to check for scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(60)