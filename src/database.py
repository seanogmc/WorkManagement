import sqlite3
from datetime import datetime, timedelta

# Connect to the database (creates shifts.db if it doesn’t exist)
conn = sqlite3.connect("C:/Users/Sean Og/Desktop/Code/WorkManager/data/shifts.db")
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
days_until_sunday = (6 - today.weekday() + 7) % 7  # Days until next Sunday
if days_until_sunday == 0:
    days_until_sunday = 7
start_date = today + timedelta(days=days_until_sunday)

test_shifts = [
    (start_date.strftime("%Y-%m-%d"), "09:00", "14:00"),  # Sunday
    ((start_date + timedelta(days=2)).strftime("%Y-%m-%d"), "13:00", "17:00"),  # Tuesday
    ((start_date + timedelta(days=4)).strftime("%Y-%m-%d"), "10:00", "15:00"),  # Thursday
]

for shift in test_shifts:
    cursor.execute("INSERT INTO shifts (date, start_time, end_time) VALUES (?, ?, ?)", shift)

conn.commit()

# Verify the data
cursor.execute("SELECT * FROM shifts")
print(cursor.fetchall())

conn.close()