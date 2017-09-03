from calendar import monthrange
import calendar
from datetime import datetime, time


def get_this_month_date_range():
    current_year_int = datetime.now().year
    current_month_int = datetime.now().month
    last_day_of_current_month = monthrange(current_year_int, current_month_int)[1]
    current_day_datetime = datetime(current_year_int, current_month_int, datetime.now().day, 00, 00, 00)
    end_of_month_datetime = datetime(datetime.now().year, datetime.now().month, last_day_of_current_month, 23, 59, 59)
    return [current_day_datetime, end_of_month_datetime]


def get_this_year_date_range():
    return [
        datetime(datetime.now().year, datetime.now().month, datetime.now().day, 00, 00, 00),
        datetime(datetime.now().year, 12, 31, 23, 59, 59)
    ]


def get_this_week_date_range():
    end_of_week_day = datetime.now().day + (7 - datetime.now().isocalendar()[2])
    return [
        datetime(datetime.now().year, datetime.now().month, datetime.now().day, 00, 00, 00),
        datetime(datetime.now().year, datetime.now().month, end_of_week_day, 23, 59, 59)
    ]


def get_today_date_range():
    return [
        datetime(datetime.now().year, datetime.now().month, datetime.now().day, 00, 00, 00),
        datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59)
    ]


def get_tomorrow_date_range():
    return [
        datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1, 00, 00, 00),
        datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1, 23, 59, 59)
    ]


def get_time_range_by_day_period(day_period):
    arg_to_time_map = {
        'morning': [time(6, 0, 0), time(11,59,59)],
        'afternoon': [time(12, 0, 0), time(17,59,59)],
        'evening': [time(18, 0, 0), time(21, 59, 59)],
        'night': [time(22, 0, 0), time(5,59,59)]
    }
    return arg_to_time_map[day_period]
