import aiohttp
from datetime import datetime
from time import strftime, gmtime
from random import choice
import os

users_dota_id = {
    'islamtramov': 70040436,
    'TikhonovD': 92183733,
    'rash708': 46482901,
    'NSIbragim': 166583635,
    'misha1234555': 67777264,
    'NikoGasanov': 181487850
}

async def update_player_matches(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.opendota.com/api/players/{users_dota_id[username]}/refresh'):
            pass


async def get_last_game_json(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.opendota.com/api/players/{users_dota_id[username]}/matches?limit=1&lobby_type=7') as response:
            last_game_json = await response.json()
            return last_game_json[0]


def check_vistory(last_game):
    victory_messages = ['разнёс бомжей', 'засолил', '2ez', 'в сола']
    defeat_messages = ['отлетел очередняра', 'заруинили', 'за тупость']

    is_victory = (last_game['radiant_win'] and last_game['player_slot'] <= 127) or (not last_game['radiant_win'] and last_game['player_slot'] > 127)
    if is_victory:
        return choice(victory_messages)
    else:
        return choice(defeat_messages)


async def get_winrate(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.opendota.com/api/players/{users_dota_id[username]}/wl?limit=20&lobby_type=7') as response:
            winrate = await response.json()
            return f"{winrate['win']}/{winrate['lose']}"


def make_statistics_message(username: str, datetime: str, duration: str, game_result: str, winrate: str):
    stat = f'Последняя игра {username}: \n'
    stat += f'Дата: {datetime} \n'
    stat += f'Длительность: {duration} \n'
    stat += f'Результат: {game_result} \n'
    stat += f'Винрейт за последние 20 игр: {winrate} \n'
    return stat


async def get_last_game_statistics(username: str):
    await update_player_matches(username)
    last_game = await get_last_game_json(username)

    last_game_date = last_game['start_time']
    pretty_datetime = datetime.fromtimestamp(last_game_date, tz=None).strftime("%d.%m.%Y, %H:%M:%S")
    duration = strftime('%H:%M:%S', gmtime(last_game['duration']))
    game_result = check_vistory(last_game)
    winrate = await get_winrate(username)

    return make_statistics_message(username, pretty_datetime, duration, game_result, winrate)
