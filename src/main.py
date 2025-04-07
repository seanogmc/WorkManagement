import threading
from gui import ShiftManagerGUI
import emailer
import tkinter as tk

def run_emailer():
    """Run the emailer in a separate thread."""
    emailer.send_weekly_email()  # For testing
    while True:
        emailer.schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Start the emailer in a background thread
    emailer_thread = threading.Thread(target=run_emailer, daemon=True)
    emailer_thread.start()

    # Start the GUI
    root = tk.Tk()
    app = ShiftManagerGUI(root)
    root.mainloop()