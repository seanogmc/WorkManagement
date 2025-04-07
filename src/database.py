import sqlite3
import os
from datetime import datetime, timedelta

# Define the database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "shifts.db")

# Print the path for debugging
print("Database path:", DB_PATH)

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT DEFAULT 'pending',
        hours REAL
    )
""")

# Clear existing data (optional, for testing)
cursor.execute("DELETE FROM shifts")

# Add test data for the next week
today = datetime.now()
days_until_sunday = (6 - today.weekday() + 7) % 7
if days_until_sunday == 0:
    days_until_sunday = 7
start_date = today + timedelta(days=days_until_sunday)

# Calculate hours for each shift
test_shifts = [
    (start_date.strftime("%d-%m-%Y"), "09:00", "14:00"),  # Changed to DD-MM-YYYY
    ((start_date + timedelta(days=2)).strftime("%d-%m-%Y"), "13:00", "17:00"),
    ((start_date + timedelta(days=4)).strftime("%d-%m-%Y"), "10:00", "15:00"),
]

for shift in test_shifts:
    date, start_time, end_time = shift
    # Calculate hours
    start_dt = datetime.strptime(f"2000-01-01 {start_time}", "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(f"2000-01-01 {end_time}", "%Y-%m-%d %H:%M")
    hours = (end_dt - start_dt).seconds / 3600
    # Insert with hours
    cursor.execute(
        "INSERT INTO shifts (date, start_time, end_time, hours) VALUES (?, ?, ?, ?)",
        (date, start_time, end_time, hours)
    )

conn.commit()

# Verify the data
cursor.execute("SELECT * FROM shifts")
print(cursor.fetchall())

conn.close()