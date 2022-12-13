from datetime import datetime, time
import random


def is_now_working_time(end_of_work: int):
    now = datetime.now().time()
    return now < time(end_of_work, 00, 00) and now > time(end_of_work - 9, 00, 00)


def get_diff_working_hours(username: str):
    stop_working = {
        'islamtramov': 18,
        'TikhonovD': 18,
        'rash708': 18,
        'NSIbragim': 19,
        'misha1234555': 19
    }

    if username in stop_working:
        now = datetime.now()
        stop = datetime.now().replace(hour=stop_working[username], minute=0, second=0)

        if not is_now_working_time(stop_working[username]):
            message = 'леее, куда прёшь, пора отдыхать'
        else:
            diff_hours = get_diff_hours(now, stop)
            message = f'до конца рабочего дня осталось: {diff_hours}'
        return message
    else:
        return ''


def is_rashid_relaxing():
    return not is_now_working_time(18)


def get_diff_hours(start, stop):
    diff = stop - start
    return str(diff).split(".")[0]


def get_special_phrase(username: str):
    special_phrases = {
        'NikoGasanov': ['отдохни от доты, брат, не сегодня'],
        'islamtramov': ['АШАЛЕТЬ']
    }

    if username in special_phrases:
        return f'{random.choice(special_phrases[username])}\n'
    else:
        return ''


def get_working_hours_info(username: str):
    message = get_special_phrase(username)
    message += get_diff_working_hours(username)

    if username != 'rash708':
        if not is_rashid_relaxing():
            message += f"\nА вот Рашиду {get_diff_working_hours('rash708')}"
        else:
            message += '\nА Рашид уже отдыхает)))'
    return message
