import schedule
import time
import datetime
from .fetcher import run_main
from .isHoliday import is_holiday


def schedule_jobs():
    print(time.strftime("%A, %B %d, %Y"))
    today_date = datetime.date.today()
    print(today_date)
    if today_date.weekday() > 4 or is_holiday(today_date):
        print("It's the weekend or a US Federal Holiday. Wall street is closed.\nBye!")
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
