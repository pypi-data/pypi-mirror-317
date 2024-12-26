import calendar
import datetime


def get_first_and_last_day():
    today = datetime.date.today()
    year = today.year
    month = today.month
    first_day = today.replace(day=1)
    last_day = today.replace(day=calendar.monthrange(year, month)[1])
    return first_day, last_day