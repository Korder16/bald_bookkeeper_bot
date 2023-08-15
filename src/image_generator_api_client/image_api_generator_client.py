from aiohttp import ClientSession
import json
import base64
import io
from os import getenv


class image_api_generator_client:

    def __init__(self) -> None:
        self.__url = getenv("IMAGE_GENERATOR_API_URL")
        self.__port = getenv("IMAGE_GENERATOR_API_PORT")
        self.__headers = {'Content-type': 'application/json'}

    def __make_url(self):
        return f'http://{self.__url}:{self.__port}'

    async def get_last_game_statistics_image(self, match_info: json) -> io.BytesIO:
        url = self.__make_url()

        endpoint = '/statistics/last_game'

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}', json=match_info, headers=self.__headers) as response:
                response = await response.json(content_type='text/html')
                return io.BytesIO(base64.b64decode(response)).getvalue()

    async def get_teammates_statistics_image(self, user_id: str, allies_info: json):
        url = self.__make_url()

        endpoint = '/statistics/teammates'

        params = {'user_id': user_id}

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}', json=allies_info, headers=self.__headers, params=params) as response:
                response = await response.json(content_type='text/html')
                return io.BytesIO(base64.b64decode(response)).getvalue()
