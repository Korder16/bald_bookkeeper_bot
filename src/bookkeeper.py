from .user_infos import user_infos
from .datetime_utils import get_day_of_week, get_hours_until_end_of_work, is_now_working_time, is_weekend
from .emoji_generator import get_emoji_number, get_emoji_by_alias, emojis
from .stickers import sticker_ids
from datetime import date
from dateutil.relativedelta import relativedelta

def is_rashid_relaxing():
    return not is_now_working_time(18)


def make_user_message(user_id: int):
    username = user_infos[user_id].name

    warning_emoji = get_emoji_by_alias(emojis['warning'])
    return f'{warning_emoji}{username}{warning_emoji}'


def get_hours_until_end_of_work_message(day_of_week: int, stop_working_hour: int):

    def make_work_state_message(hours_until_end_of_work: int, emoji_hours):
        message = f'{bang_emoji}{emoji_hours}'
        if (hours_until_end_of_work == 0) or (hours_until_end_of_work > 4):
            message += ' часов '
        elif hours_until_end_of_work == 1:
            message += ' час '
        elif (hours_until_end_of_work > 1) and (hours_until_end_of_work < 5):
            message += ' часа '

        message += f'и домой{bang_emoji}'
        return message

    bang_emoji = get_emoji_by_alias(emojis['bang'])

    if is_weekend(day_of_week) or not is_now_working_time(stop_working_hour):
        return f'{bang_emoji} время отдыхать {bang_emoji}'
    else:
        hours_until_end_of_work = get_hours_until_end_of_work(stop_working_hour)
        emoji_hours = get_emoji_number(hours_until_end_of_work)
        return make_work_state_message(hours_until_end_of_work, emoji_hours)


def get_days_until_weekend_message(day_of_week: int):

    def make_day_of_week_message(beach_emoji, day_of_week):
        day_until_weekend = 4 - day_of_week
        emoji_days = get_emoji_number(4 - day_of_week)
        message = f'{beach_emoji}{emoji_days}'
        if (day_until_weekend == 0) or (day_until_weekend > 4):
            message += ' дней '
        elif day_until_weekend == 1:
            message += ' день '
        elif (day_until_weekend > 1) and (day_until_weekend < 5):
            message += ' дня '

        message += f'и выходные{beach_emoji}'
        return message

    beach_emoji = get_emoji_by_alias(emojis['beach'])

    if is_weekend(day_of_week):
        return f'{beach_emoji} выходные {beach_emoji}'
    else:
        return make_day_of_week_message(beach_emoji, day_of_week)


def get_today_info_message(user_id: str):
    stop_working_hour = user_infos[user_id].stop_working_hour
    day_of_week = get_day_of_week()
    message_tokens = [
        make_user_message(user_id),
        get_hours_until_end_of_work_message(day_of_week, stop_working_hour),
        get_days_until_weekend_message(day_of_week)
    ]

    return '\n'.join(message_tokens)


def get_mr_incredible_sticker():
    day_of_week = get_day_of_week()
    return sticker_ids['mr_incredible'][day_of_week]


def count_days_without_marathon():
    first_time_marathon_mention = date(2016, 1, 18)
    today = date.today()
    diff = relativedelta(today, first_time_marathon_mention)
    message = 'Сколько уже ждем марафон Рашида?\n'
    message_tokens = [
        f'{diff.years} лет',
        f'{diff.months} месяцев',
        f'{diff.days} дней'
    ]

    return message + ', '.join(message_tokens)
