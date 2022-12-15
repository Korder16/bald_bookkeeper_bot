import aiohttp
from .dota_models import users_dota_id


async def update_player_matches(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.opendota.com/api/players/{users_dota_id[username]}/refresh'):
            pass


async def get_last_match_json(username: str):
    async with aiohttp.ClientSession() as session:
        last_match_id = ''
        async with session.get(f'https://api.opendota.com/api/players/{users_dota_id[username]}/matches?limit=1&lobby_type=7') as response:
            last_match_json = await response.json()
            last_match_id = last_match_json[0]['match_id']

        async with session.get(f'https://api.opendota.com/api/matches/{last_match_id}') as response:
            return await response.json()


async def get_winrate(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.opendota.com/api/players/{users_dota_id[username]}/wl?limit=20&lobby_type=7') as response:
            winrate = await response.json()
            return f"{winrate['win']}/{winrate['lose']}"
