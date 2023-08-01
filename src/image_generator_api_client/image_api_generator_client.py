from aiohttp import ClientSession
import json
import base64
import io


class image_api_generator_client:

    def __init__(self) -> None:
        self.__url = '185.189.167.54'
        self.__port = 5001
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

    async def get_teammates_statistics_image(self, allies_info: json):
        url = self.__make_url()

        endpoint = '/statistics/teammates'

        async with ClientSession() as session:
            async with session.get(url=f'{url}{endpoint}', json=allies_info, headers=self.__headers) as response:
                response = await response.json(content_type='text/html')
                return io.BytesIO(base64.b64decode(response)).getvalue()
