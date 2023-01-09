from datetime import datetime, time
import random
import json

with open('user_infos.json', 'r') as f:
    user_infos = json.load(f)

def is_now_working_time(end_of_work: int):
    now = datetime.now().time()
    return now < time(end_of_work, 00, 00) and now > time(end_of_work - 9, 00, 00)


def get_diff_working_hours(user_id: int):
    if user_id in user_infos:
        now = datetime.now()
        stop = datetime.now().replace(hour=user_infos[user_id]['stop_working_hour'], minute=0, second=0)

        if not is_now_working_time(user_infos[user_id]['stop_working_hour']):
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


def get_special_phrase(user_id: int):
    special_phrases = {
        234173758: ['отдохни от доты, брат, не сегодня'],
        406351790: ['АШАЛЕТЬ']
    }

    if user_id in special_phrases:
        return f'{random.choice(special_phrases[user_id])}\n'
    else:
        return ''


def get_working_hours_info(user_id: str):
    username = user_infos[user_id]['name']
    message = f'{username}, '
    message += get_special_phrase(user_id)
    message += get_diff_working_hours(user_id)

    if username != 'Рашид':
        if not is_rashid_relaxing():
            message += f"\nА вот Рашиду {get_diff_working_hours('178513005')}"
        else:
            message += '\nА Рашид уже отдыхает)))'
    return message
