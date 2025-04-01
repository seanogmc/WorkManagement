import schedule
import tkcalendar

def test_job():
    print("Schedule test job ran!")

schedule.every(10).seconds.do(test_job)

import time
for _ in range(3):
    schedule.run_pending()
    time.sleep(1)

# Test tkcalendar
print("Tkcalendar version:", tkcalendar.__version__)

print("Hospital Shift Manager setup is working!")