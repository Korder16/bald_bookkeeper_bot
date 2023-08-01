import requests
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

    def get_last_game_statistics_image(self, match_info: json) -> io.BytesIO:
        url = self.__make_url()

        response = requests.get(f'{url}/statistics/last_game', json=match_info, headers=self.__headers)
        return io.BytesIO(base64.b64decode(response.json())).getvalue()

    def get_teammates_statistics_image(self, allies_info: json):
        url = self.__make_url()

        response = requests.get(f'{url}/statistics/teammates', json=allies_info, headers=self.__headers)
        return io.BytesIO(base64.b64decode(response.json())).getvalue()
