from aiohttp import ClientSession
from ..config import load_config

class image_api_generator_client:

    def __init__(self) -> None:
        config = load_config()
        self.__url = config.image_generator_config.host
        self.__port = config.image_generator_config.port
        self.__headers = {'Content-type': 'application/json'}

    def __make_url(self):
        return f'http://{self.__url}:{self.__port}'

    async def get_last_game_statistics_image(self, dota_account_id):
        url = self.__make_url()
        endpoint = '/statistics/last_game'

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}?player_id={dota_account_id}', headers=self.__headers) as response:
                return await response.json(content_type=None)

    async def get_teammates_statistics_image(self, player_id: str):
        url = self.__make_url()

        endpoint = f'/statistics/teammates'

        params = {'player_id': player_id}

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}', headers=self.__headers, params=params) as response:
                return await response.json(content_type=None)
