from aiohttp import ClientSession
import asyncio
from ..sql_client import bald_bookeeper_bot_db_client


class opendota_api_client:

    def __init__(self) -> None:
        self.__url = 'https://api.opendota.com/api'

    async def update_last_match_info(self, user_id: str):
        endpoint = f'/players/{user_id}/refresh'

        async with ClientSession() as session:
            async with session.post(f'{self.__url}{endpoint}'):
                pass

    async def get_last_ranked_match(self, user_id: str):
        endpoint = f'/players/{user_id}/matches?limit=1&lobby_type=7'

        async with ClientSession() as session:
            async with session.get(f'{self.__url}{endpoint}') as response:
                last_match_json = await response.json()
                return last_match_json[0]

    async def get_last_ranked_match_info(self, last_match_id: str):
        endpoint = f'/matches/{last_match_id}'

        async with ClientSession() as session:
            async with session.get(f'{self.__url}{endpoint}') as response:
                return await response.json()

    async def get_allies_info(self, user_id: str):
        endpoint = f'/players/{user_id}/peers?&lobby_type=7&date=14'

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

    async def get_allies_statistics_json(self, user_id: str):

        dota_user_id = await bald_bookeeper_bot_db_client().get_dota_id_by_tg_id(user_id)

        tasks = [
            asyncio.ensure_future(self.update_last_match_info(dota_user_id)),
            asyncio.ensure_future(self.get_allies_info(dota_user_id))
        ]

        alies_statistics = await asyncio.gather(*tasks)
        return alies_statistics[-1]


def is_win_game(is_radiant_win: bool, player_slot: int):
    return (is_radiant_win and player_slot <= 127) or (not is_radiant_win and player_slot > 128)


async def get_last_match_results(user_id: str):
    client = opendota_api_client()
    return await client.get_last_match_json(user_id)


async def get_allies_info_for_last_two_weeks(user_id: str):
    client = opendota_api_client()
    return await client.get_allies_statistics_json(user_id)
