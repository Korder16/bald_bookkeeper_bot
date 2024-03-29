from aiohttp import ClientSession
import json
import base64
import io
from ..config import load_config


class image_api_generator_client:

    def __init__(self) -> None:
        config = load_config()
        self.__url = config.image_generator_config.host
        self.__port = config.image_generator_config.port
        self.__headers = {'Content-type': 'application/json'}

    def __make_url(self):
        return f'http://{self.__url}:{self.__port}'

    async def get_last_game_statistics_image(self, last_match_results: json) -> io.BytesIO:
        url = self.__make_url()
        endpoint = '/statistics/last_game'

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}', json=last_match_results, headers=self.__headers) as response:
                response = await response.json(content_type=None)
                return io.BytesIO(base64.b64decode(response)).getvalue()

    async def get_teammates_statistics_image(self, user_id: str, allies_info: json):
        url = self.__make_url()

        endpoint = '/statistics/teammates'

        params = {'user_id': user_id}

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}', json=allies_info, headers=self.__headers, params=params) as response:
                response = await response.json(content_type=None)
                result = io.BytesIO(base64.b64decode(response))
                return result.getvalue()
