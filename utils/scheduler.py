import schedule
import time
from .fetcher import run_main

def schedule_jobs():
    # Run the task starting from 9 am every 1 hour until 4 pm
    for hour in range(9, 16):  # 16 is exclusive
        formatted_hour = f"{hour:02}"
        print(f"Running at {formatted_hour}:00:00")
        try:
            schedule.every().monday.at(f"{formatted_hour}:00:00").do(run_main)
            schedule.every().tuesday.at(f"{formatted_hour}:00:00").do(run_main)
            schedule.every().wednesday.at(f"{formatted_hour}:00:00").do(run_main)
            schedule.every().thursday.at(f"{formatted_hour}:00:00").do(run_main)
            schedule.every().friday.at(f"{formatted_hour}:00:00").do(run_main)
        except schedule.ScheduleValueError as e:
            print(f"Failed to schedule the job for {formatted_hour}:00:00 due to: {e}")

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
