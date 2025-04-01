import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime

class ShiftManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Shift Manager")

        # Create the calendar
        self.cal = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=10)

        # Start time entry
        tk.Label(self.root, text="Start Time (HH:MM):").pack()
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.insert(0, "09:00")  # Default start time
        self.start_time_entry.pack()

        # End time entry
        tk.Label(self.root, text="End Time (HH:MM):").pack()
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.insert(0, "14:00")  # Default end time
        self.end_time_entry.pack()

        # Save button
        tk.Button(self.root, text="Save Availability", command=self.save_availability).pack(pady=10)

        # Display saved shifts
        tk.Label(self.root, text="Saved Shifts:").pack()
        self.shift_display = tk.Text(self.root, height=10, width=50)
        self.shift_display.pack(pady=10)

        # Load existing shifts on startup
        self.load_shifts()

    def save_availability(self):
        """Save the selected date and times to the database."""
        selected_date = self.cal.get_date()
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
        hours = (end_dt - start_dt).seconds / 3600  # Convert to hours

        # Save to database
        try:
            conn = sqlite3.connect("C:/Users/Sean Og/Desktop/Code/WorkManager/data/shifts.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shifts (date, start_time, end_time, hours) VALUES (?, ?, ?, ?)",
                (selected_date, start_time, end_time, hours)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Availability saved for {selected_date}")
            self.load_shifts()  # Refresh the display
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def load_shifts(self):
        """Load and display all shifts from the database."""
        self.shift_display.delete(1.0, tk.END)  # Clear the display
        try:
            conn = sqlite3.connect("C:/Users/Sean Og/Desktop/Code/WorkManager/data/shifts.db")
            cursor = conn.cursor()
            cursor.execute("SELECT date, start_time, end_time, hours FROM shifts ORDER BY date")
            shifts = cursor.fetchall()
            conn.close()

            if not shifts:
                self.shift_display.insert(tk.END, "No shifts saved yet.")
            else:
                for shift in shifts:
                    date, start_time, end_time, hours = shift
                    self.shift_display.insert(tk.END, f"{date}: {start_time} - {end_time} ({hours:.1f} hours)\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load shifts: {e}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftManagerGUI(root)
    root.mainloop()