import schedule
import time
import datetime
from .fetcher import run_main


def schedule_jobs():
    print(time.strftime("%A, %B %d, %Y"))
    print(time.strftime("%m/%d/%Y"))
    if datetime.datetime.now().weekday() > 4:
        print("It's the weekend. Wall street is closed.\nBye!")
        return

    # Schedule the task to run every 30 minutes from 9:30 AM to 4:00 PM
    start_hour = 9
    start_minute = 30
    end_hour = 16
    interval = 30  # minutes

    while start_hour < end_hour or (start_hour == end_hour and start_minute == 0):
        # Format time string
        time_string = f"{start_hour:02}:{start_minute:02}"

        # Schedule for each weekday
        schedule.every().monday.at(time_string).do(run_main)
        schedule.every().tuesday.at(time_string).do(run_main)
        schedule.every().wednesday.at(time_string).do(run_main)
        schedule.every().thursday.at(time_string).do(run_main)
        schedule.every().friday.at(time_string).do(run_main)

        print(f"Scheduled for {time_string}")

        # Increment time
        start_minute += interval
        if start_minute >= 60:
            start_hour += 1
            start_minute -= 60

    # Keep the script running and check for pending jobs
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second


# def schedule_jobs():
#     # print the current day of the week in day of the week + M/D/YY format
#     print(time.strftime("%A, %B %d, %Y"))
#     print(time.strftime("%m/%d/%Y"))

#     # Run the task starting from 9 am every 1 hour until 4 pm
#     for hour in range(9, 17):  # 16 is exclusive
#         formatted_hour = f"{hour:02}"
#         print(f"Running at {formatted_hour}:00:00")
#         try:
#             schedule.every().monday.at(f"{formatted_hour}:00:00").do(run_main)
#             schedule.every().tuesday.at(f"{formatted_hour}:00:00").do(run_main)
#             schedule.every().wednesday.at(f"{formatted_hour}:00:00").do(run_main)
#             schedule.every().thursday.at(f"{formatted_hour}:00:00").do(run_main)
#             schedule.every().friday.at(f"{formatted_hour}:00:00").do(run_main)
#         except schedule.ScheduleValueError as e:
#             print(f"Failed to schedule the job for {formatted_hour}:00:00 due to: {e}")

#     # Keep the script running
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
