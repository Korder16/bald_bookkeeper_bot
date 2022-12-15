import json
import requests
from pathlib import Path
from PIL import Image


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


def download_item_icons():
    path = 'media/item_icons'
    if not Path(path).exists():
        Path.mkdir(path)

    with open('item_ids.json') as f:
        data = json.load(f)

    for value in data.values():
        download_item_icon(value)
        print(f'{value} icon downloaded')


def download_hero_icons():
    path = 'media/hero_icons'
    if not Path(path).exists():
        Path.mkdir(path)

    with open('heroes.json') as f:
        data = json.load(f)

    for value in data.values():
        hero_name = value['name']
        download_hero_icon(hero_name)
        print(f'{hero_name} icon downloaded')


if __name__ == '__main__':
    download_hero_icons()
    download_item_icons()
