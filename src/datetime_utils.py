from datetime import datetime, time
from pytz import timezone


def get_timezone():
    return timezone('Europe/Moscow')


def get_day_of_week():
    return datetime.now().weekday()


def is_weekend(day: int):
    return day > 4


def get_day_of_week_name():
    russian_weekdays = {
        0: 'понедельник',
        1: 'вторник',
        2: 'среда',
        3: 'четверг',
        4: 'пятница',
        5: 'суббота',
        6: 'воскресенье'
    }

    weekday_index = get_day_of_week()
    return russian_weekdays[weekday_index]


def is_now_working_time(end_of_work: int):
    tz = get_timezone()
    now = datetime.now(tz).time()
    return now < time(end_of_work, 00, 00) and now > time(end_of_work - 9, 00, 00)


def get_hours_until_end_of_work(stop_working_hour):
    tz = get_timezone()
    now = datetime.now(tz)
    stop = datetime.now(tz).replace(hour=stop_working_hour, minute=0, second=0)

    delta = stop - now
    return round(delta.total_seconds() / (60 * 60))
