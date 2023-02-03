from .user_infos import user_infos
from .datetime_utils import get_day_of_week, get_days_until_weekend, get_hours_until_end_of_work, is_now_working_time
from .emoji_generator import get_emoji_number, get_warning_emoji, get_bang_emoji, get_beach_emoji
from .stickers import get_mr_incredible_sticker_id


def is_rashid_relaxing():
    return not is_now_working_time(18)


def get_user_message(user_id: int):
    username = user_infos[user_id].name
    warning_emoji = get_warning_emoji()
    return f'{warning_emoji}{username}{warning_emoji}'


def get_hours_until_end_of_work_message(stop_working_hour: int):
    if is_now_working_time(stop_working_hour):
        hours_until_end_of_work = get_hours_until_end_of_work(stop_working_hour)
        emoji_hours = get_emoji_number(hours_until_end_of_work)
        bang_emoji = get_bang_emoji()

        message = f'{bang_emoji}{emoji_hours}'
        if (hours_until_end_of_work == 0) or (hours_until_end_of_work > 4):
            message += ' часов '
        elif hours_until_end_of_work == 1:
            message += ' час '
        elif (hours_until_end_of_work > 1) and (hours_until_end_of_work < 5):
            message += ' часа '

        message += f'и домой{bang_emoji}'
        return message
    else:
        return f'{bang_emoji} время отдыхать {bang_emoji}'


def get_days_until_weekend_message():
    beach_emoji = get_beach_emoji()
    days_until_weekend = get_days_until_weekend()
    emoji_days = get_emoji_number(days_until_weekend)

    message = f'{beach_emoji}{emoji_days}'
    if (days_until_weekend == 0) or (days_until_weekend > 4):
        message += ' дней '
    elif days_until_weekend == 1:
        message += ' день '
    elif (days_until_weekend > 1) and (days_until_weekend < 5):
        message += ' дня '

    message += f'и выходные{beach_emoji}'
    return message


def get_today_info_message(user_id: str):
    stop_working_hour = user_infos[user_id].stop_working_hour
    message_tokens = [
        get_user_message(user_id),
        get_hours_until_end_of_work_message(stop_working_hour),
        get_days_until_weekend_message()
    ]

    return '\n'.join(message_tokens)


def get_mr_incredible_sticker():
    today = get_day_of_week()
    return get_mr_incredible_sticker_id(today)
