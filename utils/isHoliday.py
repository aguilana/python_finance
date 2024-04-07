import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar


def is_holiday(date):
    cal = USFederalHolidayCalendar()

    holidays = cal.holidays(start=date, end=date)

    return not holidays.empty
