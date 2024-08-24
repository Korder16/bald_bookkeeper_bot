from .datetime_utils import (
    get_day_of_week,
    get_hours_until_end_of_work,
    is_now_working_time,
    is_weekend,
)
from .emoji_generator import get_emoji_number, get_emoji_by_alias, emojis
from .stickers import sticker_ids
from datetime import date
from dateutil.relativedelta import relativedelta
from random import choice
from .sql_client import bald_bookeeper_bot_db_client


def is_rashid_relaxing():
    return not is_now_working_time(18)


async def make_user_message(user_id: int, db_connection):
    db_client = bald_bookeeper_bot_db_client(db_connection)
    username = await db_client.get_username_by_tg_id(user_id)

    warning_emoji = get_emoji_by_alias(emojis["warning"])
    return f"{warning_emoji}{username}{warning_emoji}"


def get_hours_until_end_of_work_message(day_of_week: int, stop_working_hour: int):

    def make_work_state_message(hours_until_end_of_work: int, emoji_hours):
        message = f"{bang_emoji}{emoji_hours}"
        if (hours_until_end_of_work == 0) or (hours_until_end_of_work > 4):
            message += " часов "
        elif hours_until_end_of_work == 1:
            message += " час "
        elif (hours_until_end_of_work > 1) and (hours_until_end_of_work < 5):
            message += " часа "

        message += f"и домой{bang_emoji}"
        return message

    bang_emoji = get_emoji_by_alias(emojis["bang"])

    if is_weekend(day_of_week) or not is_now_working_time(stop_working_hour):
        return f"{bang_emoji} время отдыхать {bang_emoji}"
    else:
        hours_until_end_of_work = get_hours_until_end_of_work(stop_working_hour)
        emoji_hours = get_emoji_number(hours_until_end_of_work)
        return make_work_state_message(hours_until_end_of_work, emoji_hours)


def get_days_until_weekend_message(day_of_week: int):

    def make_day_of_week_message(beach_emoji, day_of_week):
        day_until_weekend = 4 - day_of_week
        emoji_days = get_emoji_number(4 - day_of_week)
        message = f"{beach_emoji}{emoji_days}"
        if (day_until_weekend == 0) or (day_until_weekend > 4):
            message += " дней "
        elif day_until_weekend == 1:
            message += " день "
        elif (day_until_weekend > 1) and (day_until_weekend < 5):
            message += " дня "

        message += f"и выходные{beach_emoji}"
        return message

    beach_emoji = get_emoji_by_alias(emojis["beach"])

    if is_weekend(day_of_week):
        return f"{beach_emoji} выходные {beach_emoji}"
    else:
        return make_day_of_week_message(beach_emoji, day_of_week)


async def get_today_info_message(user_id: int, db_connection):
    db_client = bald_bookeeper_bot_db_client(db_connection)
    stop_working_hour = await db_client.get_stop_working_hour_by_tg_id(user_id)

    day_of_week = get_day_of_week()
    message_tokens = [
        await make_user_message(user_id, db_connection),
        get_hours_until_end_of_work_message(day_of_week, stop_working_hour),
        get_days_until_weekend_message(day_of_week),
    ]

    return "\n".join(message_tokens)


def get_mr_incredible_sticker():
    day_of_week = get_day_of_week()
    return sticker_ids["mr_incredible"][day_of_week]


def make_date_message(diff):
    message_tokens = [
        f"{diff.years} лет",
        f"{diff.months} месяцев",
        f"{diff.days} дней",
    ]

    return ", ".join(message_tokens)


def count_date_diff(date_from: date):
    return relativedelta(date.today(), date_from)


def count_days_without_marathon():
    first_time_marathon_mention = date(2016, 1, 18)
    diff = count_date_diff(first_time_marathon_mention)
    message_headers = [
        "Сколько уже ждем марафон Рашида?",
        "Рашид воздуханит насчёт марафона уже",
        "Рашид не держит слово на протяжении",
        "С момента как Рашид наебал Михана прошло уже",
        "Рашид и марафон доты не могут встретиться на протяжении",
    ]

    return f"{choice(message_headers)}\n" + make_date_message(diff)


def count_day_from_ex_ancient():
    last_time_ancient = date(2019, 10, 19)
    diff = count_date_diff(last_time_ancient)

    return "Михан бывший властелин уже\n" + make_date_message(diff)
