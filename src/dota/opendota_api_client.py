from aiohttp import ClientSession
import asyncio
import json
from ..sql_client import bald_bookeeper_bot_db_client
from tabulate import tabulate

class opendota_api_client:

    def __init__(self) -> None:
        self.__url = 'https://api.opendota.com/api'

    async def update_last_match_info(self, user_id: str):
        endpoint = f'/players/{user_id}/refresh'

        async with ClientSession() as session:
            async with session.post(f'{self.__url}{endpoint}'):
                pass

    async def get_last_ranked_match(self, user_id: str):
        endpoint = f'/players/{user_id}/matches?limit=1&significant=0'
        async with ClientSession() as session:
            async with session.get(f'{self.__url}{endpoint}') as response:
                last_match_json = await response.json()
                return last_match_json[0]

    async def get_last_ranked_match_info(self, last_match_id: str):
        endpoint = f'/matches/{last_match_id}'

        async with ClientSession() as session:
            async with session.get(f'{self.__url}{endpoint}') as response:
                return await response.json()

    async def get_allies_info(self, user_id: str, date: int):
        endpoint = f'/players/{user_id}/peers?&lobby_type=7&date={date}'

        async with ClientSession() as session:
            async with session.get(f'{self.__url}{endpoint}') as response:
                return await response.json()

    async def get_player_totals(self, user_id: str):
        endpoint = f'/players/{user_id}/totals?&lobby_type=7&date=365'

        async with ClientSession() as session:
            async with session.get(f'{self.__url}{endpoint}') as response:
                return await response.json()

    async def get_last_match_json(self, user_id: str):
        db_client = bald_bookeeper_bot_db_client()
        dota_user_id = await db_client.get_dota_id_by_tg_id(user_id)

        last_match_id = ''

        tasks = [
            asyncio.ensure_future(self.update_last_match_info(dota_user_id)),
            asyncio.ensure_future(self.get_last_ranked_match(dota_user_id))
        ]

        last_ranked_match = await asyncio.gather(*tasks)

        last_match_id = last_ranked_match[-1]['match_id']
        await db_client.update_last_match_id(dota_user_id, last_match_id)

        is_win = is_win_game(last_ranked_match[-1]['radiant_win'], last_ranked_match[-1]['player_slot'])

        last_ranked_match_info = await asyncio.gather(*[asyncio.ensure_future(self.get_last_ranked_match_info(last_match_id))])
        return last_ranked_match_info[-1], is_win

    async def get_allies_statistics_json(self, user_id: str, date: int):

        dota_user_id = await bald_bookeeper_bot_db_client().get_dota_id_by_tg_id(user_id)

        tasks = [
            asyncio.ensure_future(self.update_last_match_info(dota_user_id)),
            asyncio.ensure_future(self.get_allies_info(dota_user_id, date))
        ]

        alies_statistics = await asyncio.gather(*tasks)
        return alies_statistics[-1]

    async def get_player_totals_json(self, user_id: str):

        dota_user_id = await bald_bookeeper_bot_db_client().get_dota_id_by_tg_id(user_id)

        tasks = [
            asyncio.ensure_future(self.update_last_match_info(dota_user_id)),
            asyncio.ensure_future(self.get_player_totals(dota_user_id))
        ]

        player_totals = await asyncio.gather(*tasks)
        return player_totals[-1]


def is_win_game(is_radiant_win: bool, player_slot: int):
    return (is_radiant_win and player_slot <= 127) or (not is_radiant_win and player_slot > 128)


async def get_last_match_results(user_id: str):
    client = opendota_api_client()
    return await client.get_last_match_json(user_id)


async def get_allies_info_for_last_two_weeks(user_id: str):
    client = opendota_api_client()
    return await client.get_allies_statistics_json(user_id, 14)


async def get_allies_info_for_last_year(user_id: str):
    client = opendota_api_client()
    return await client.get_allies_statistics_json(user_id, 365)

def prepare_player_totals_for_last_year_info(player_totals: json) -> dict:
    prepared_totals = {}
    for key in player_totals:
        prepared_totals[key['field']] = {
            'sum': key['sum'],
            'n': key['n']
        }

    return prepared_totals

def generate_player_totals_for_last_year_message(prepared_player_totals: dict):
    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    def calculate_avg(sum: int, n: int):
        if n == 0:
            return 0
        else:
            return sum / n

    mappings = {
        'Убийств': {
            'overall': prepared_player_totals['kills']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['kills']['sum'], prepared_player_totals['kills']['n']), 2)
        },
        'Ассистов': {
            'overall': prepared_player_totals['assists']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['assists']['sum'], prepared_player_totals['assists']['n']), 2)
        },
        'Смертей': {
            'overall': prepared_player_totals['deaths']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['deaths']['sum'], prepared_player_totals['deaths']['n']), 2)
        },
        'КДА': {
            'overall': prepared_player_totals['kda']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['kda']['sum'], prepared_player_totals['kda']['n']), 2)
        },
        'Ластхитов': {
            'overall': human_format(prepared_player_totals['last_hits']['sum']),
            'avg_per_game': round(calculate_avg(prepared_player_totals['last_hits']['sum'], prepared_player_totals['last_hits']['n']), 2)
        },
        'Денаев': {
            'overall': human_format(prepared_player_totals['denies']['sum']),
            'avg_per_game': round(calculate_avg(prepared_player_totals['denies']['sum'], prepared_player_totals['denies']['n']), 2)
        },
        'Урона по героям': {
            'overall': human_format(prepared_player_totals['hero_damage']['sum']),
            'avg_per_game': round(calculate_avg(prepared_player_totals['hero_damage']['sum'], prepared_player_totals['hero_damage']['n']), 2)
        },
        'Урона по строениям': {
            'overall': human_format(prepared_player_totals['tower_damage']['sum']),
            'avg_per_game': round(calculate_avg(prepared_player_totals['tower_damage']['sum'], prepared_player_totals['tower_damage']['n']), 2)
        },
        'Лечение героев': {
            'overall': human_format(prepared_player_totals['hero_healing']['sum']),
            'avg_per_game': round(calculate_avg(prepared_player_totals['hero_healing']['sum'], prepared_player_totals['hero_healing']['n']), 2)
        },
        'GPM': {
            'overall': prepared_player_totals['gold_per_min']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['gold_per_min']['sum'], prepared_player_totals['gold_per_min']['n']), 2)
        },
        'XPM': {
            'overall': prepared_player_totals['xp_per_min']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['xp_per_min']['sum'], prepared_player_totals['xp_per_min']['n']), 2)
        },
        'APM': {
            'overall': prepared_player_totals['actions_per_min']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['actions_per_min']['sum'], prepared_player_totals['actions_per_min']['n']), 2)
        },
        'Убийств (курьеров)': {
            'overall': prepared_player_totals['courier_kills']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['courier_kills']['sum'], prepared_player_totals['courier_kills']['n']), 2)
        },
        'Куплено рапир': {
            'overall': prepared_player_totals['purchase_rapier']['sum'],
            'avg_per_game': round(calculate_avg(prepared_player_totals['purchase_rapier']['sum'], prepared_player_totals['purchase_rapier']['n']), 2)
        }
    }

    headers = ['', 'Всего', 'В среднем за игру']
    table = []
    for mapping in mappings:
        table.append([mapping, mappings[mapping]['overall'], mappings[mapping]['avg_per_game']])

    return f"<pre>{tabulate(table, headers, tablefmt='github')}</pre>"

async def get_player_totals_for_last_year(user_id: str):
    client = opendota_api_client()
    player_totals_json = await client.get_player_totals_json(user_id)
    prepared_player_totals_json =  prepare_player_totals_for_last_year_info(player_totals_json)
    return generate_player_totals_for_last_year_message(prepared_player_totals_json)