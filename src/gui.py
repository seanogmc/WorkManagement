import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
import os
import json

# Define the database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "shifts.db")

class ShiftManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Shift Manager")

        # Load pay rate from config
        with open(os.path.join(BASE_DIR, "config", "config.json"), "r") as f:
            config = json.load(f)
        self.pay_rate = config["pay_rate"]

        # Create the calendar with DD-MM-YYYY format
        self.cal = Calendar(self.root, selectmode="day", date_pattern="dd-mm-yyyy")
        self.cal.pack(pady=10)

        # Start time entry
        tk.Label(self.root, text="Start Time (HH:MM):").pack()
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.insert(0, "09:00")
        self.start_time_entry.pack()

        # End time entry
        tk.Label(self.root, text="End Time (HH:MM):").pack()
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.insert(0, "14:00")
        self.end_time_entry.pack()

        # Save button
        tk.Button(self.root, text="Save Availability", command=self.save_availability).pack(pady=5)

        # Report button
        tk.Button(self.root, text="Generate Monthly Report", command=self.generate_report).pack(pady=5)

        # Display saved shifts
        tk.Label(self.root, text="Saved Shifts:").pack()
        self.shift_display = tk.Text(self.root, height=10, width=50)
        self.shift_display.pack(pady=10)

        # Load existing shifts on startup
        self.load_shifts()

    def save_availability(self):
        """Save the selected date and times to the database."""
        selected_date = self.cal.get_date()  # Already in DD-MM-YYYY format
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        # Validate time format
        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Please enter times in HH:MM format (e.g., 09:00)")
            return

        # Calculate hours
        start_dt = datetime.strptime(f"2000-01-01 {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"2000-01-01 {end_time}", "%Y-%m-%d %H:%M")
        if end_dt <= start_dt:
            messagebox.showerror("Error", "End time must be after start time")
            return
        hours = (end_dt - start_dt).seconds / 3600

        # Save to database
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shifts (date, start_time, end_time, hours) VALUES (?, ?, ?, ?)",
                (selected_date, start_time, end_time, hours)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Availability saved for {selected_date}")
            self.load_shifts()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def load_shifts(self):
        """Load and display all shifts from the database."""
        self.shift_display.delete(1.0, tk.END)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT date, start_time, end_time, hours FROM shifts ORDER BY date")
            shifts = cursor.fetchall()
            conn.close()

            if not shifts:
                self.shift_display.insert(tk.END, "No shifts saved yet.")
            else:
                for shift in shifts:
                    date, start_time, end_time, hours = shift
                    hours_display = hours if hours is not None else 0.0
                    self.shift_display.insert(tk.END, f"{date}: {start_time} - {end_time} ({hours_display:.1f} hours)\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load shifts: {e}")

    def generate_report(self):
        """Generate a monthly report of hours and expected pay."""
        today = datetime.now()
        year = today.year
        month = today.month

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            # Convert DD-MM-YYYY to YYYY-MM-DD for SQLite's strftime
            cursor.execute("""
                SELECT date, start_time, end_time, hours 
                FROM shifts 
                WHERE strftime('%Y-%m', 
                              substr(date, 7, 4) || '-' || 
                              substr(date, 4, 2) || '-' || 
                              substr(date, 1, 2)) = ?
                """, (f"{year}-{month:02d}",))
            shifts = cursor.fetchall()
            conn.close()

            if not shifts:
                messagebox.showinfo("Report", "No shifts found for this month.")
                return

            total_hours = sum(shift[3] for shift in shifts if shift[3] is not None)
            expected_pay = total_hours * self.pay_rate

            report = f"Monthly Report for {month:02d}-{year}\n"  # Updated to MM-YYYY
            report += f"Total Hours: {total_hours:.1f}\n"
            report += f"Expected Pay: £{expected_pay:.2f}\n\n"
            report += "Breakdown:\n"
            for shift in shifts:
                date, start_time, end_time, hours = shift
                hours_display = hours if hours is not None else 0.0
                report += f"- {date}: {start_time} - {end_time} ({hours_display:.1f} hours)\n"

            messagebox.showinfo("Monthly Report", report)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftManagerGUI(root)
    root.mainloop()