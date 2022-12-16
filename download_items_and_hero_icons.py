import json
import requests
from pathlib import Path
from PIL import Image
from collections import deque


def download_icon(url: str, path: str):
    response = requests.get(url, stream=True).raw

    img = Image.open(response)
    img.save(path, format='webp')


def download_item_icon(item_name: str):
    if 'recipe' in item_name:
        image_url = 'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/recipe.png'
    else:
        image_url = f'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/{item_name}.png'

    path = f'media/item_icons/{item_name}.webp'
    download_icon(image_url, path)


def download_hero_icon(hero_name: str):
    image_url = f'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/{hero_name}.png'

    path = f'media/hero_icons/{hero_name}.webp'
    download_icon(image_url, path)


def download_icons(path: str, json_ids: str, func):
    if not Path(path).exists():
        Path.mkdir(path)

    with open(json_ids) as f:
        data = json.load(f)

    deque(map(func, data.values()))
    print(f'{path} icons downloaded')


if __name__ == '__main__':
    if not Path('media').exists():
        Path.mkdir('media')

    download_icons('media/hero_icons', 'heroes_ids.json', download_hero_icon)
    download_icons('media/item_icons', 'item_ids.json', download_item_icon)
