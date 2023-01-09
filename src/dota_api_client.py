import aiohttp
import asyncio
from .dota_models import user_dota_ids

async def update_last_match_info(session, user_id: str):
    async with session.post(f'https://api.opendota.com/api/players/{user_id}/refresh'):
            pass

async def get_last_ranked_match_id(session, user_id: str):
    async with session.get(f'https://api.opendota.com/api/players/{user_id}/matches?limit=1&lobby_type=7') as response:
            last_match_json = await response.json()
            return last_match_json[0]['match_id']

async def get_last_ranked_match_info(session, last_match_id: str):
    async with session.get(f'https://api.opendota.com/api/matches/{last_match_id}') as response:
            return await response.json()

async def get_allies_info(session, user_id: str):
    async with session.get(f'https://api.opendota.com/api/players/{user_id}/peers?&lobby_type=7') as response:
            return await response.json()

async def get_last_match_json(user_id: str):
    dota_user_id = user_dota_ids[user_id]
    last_match_id = ''
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(update_last_match_info(session, dota_user_id)),
            asyncio.ensure_future(get_last_ranked_match_id(session, dota_user_id))
        ]
        
        last_match_id = await asyncio.gather(*tasks)
        last_ranked_match_info = await asyncio.gather(*[asyncio.ensure_future(get_last_ranked_match_info(session, last_match_id[-1]))])
        return last_ranked_match_info[-1]


async def get_allies_statistics_json(user_id: str):
    dota_user_id = user_dota_ids[user_id]

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(update_last_match_info(session, dota_user_id)),
            asyncio.ensure_future(get_allies_info(session, dota_user_id))
        ]
        
        alies_statistics = await asyncio.gather(*tasks)
        return alies_statistics[-1]

async def get_winrate(user_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.opendota.com/api/players/{user_dota_ids[user_id]}/wl?limit=20&lobby_type=7') as response:
            winrate = await response.json()
            return f"{winrate['win']}/{winrate['lose']}"
