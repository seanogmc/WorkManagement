# Hospital Shift Manager

## Project Goal
The **Hospital Shift Manager** is a Python application designed to help hospital staff manage their shift schedules efficiently. The primary goal of this project is to simplify the process of submitting weekly availability to hospital management and tracking hours worked for payroll purposes. It provides a user-friendly graphical interface to input availability, automatically emails the schedule to a designated recipient, and generates monthly reports of hours worked and expected pay.

This tool is particularly useful for hospital workers who need to submit their availability on a regular basis and want to keep track of their hours and earnings without manual calculations.

## Features
- **Graphical User Interface (GUI)**: A simple interface built with Tkinter and `tkcalendar` to input shift availability (date, start time, and end time).
- **Database Storage**: Stores shift data in an SQLite database (`shifts.db`) for persistence.
- **Automatic Email Notifications**: Sends weekly availability emails to a specified recipient every Thursday at 9:00 AM using an SMTP server (e.g., Gmail).
- **Monthly Reports**: Generates a report of total hours worked and expected pay for the current month, based on a configurable pay rate.
- **Custom Date Format**: Dates are displayed and stored in the `DD-MM-YYYY` format (e.g., 13-04-2025) for user convenience.

## Project Structure
WorkManager/
├── src/
│   ├── main.py         # Entry point to launch the GUI and emailer
│   ├── database.py     # Initializes the SQLite database and adds test data
│   ├── gui.py          # GUI for entering and viewing shift availability
│   └── emailer.py      # Handles sending weekly availability emails
├── data/
│   └── shifts.db       # SQLite database for storing shift data
├── config/
│   └── config.json     # Configuration file for email settings and pay rate
└── README.md           # Project documentation
