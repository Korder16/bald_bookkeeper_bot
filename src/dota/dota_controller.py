import json
import io

from .dota_models import match_info, player_info, allies_statistics, ally_info
from ..image_generator import image_generator, statistics_image_generator, image_generator_settings, dota_objects_parser, fonts, text_colors
from .dota_api_client import get_last_match_json, get_allies_statistics_json
from ..user_infos import user_infos


def image_to_bytes(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='webp')
    return img_bytes.getvalue()


def parse_last_match(last_match: json, user_id: str):
    players = last_match['players']

    for player in players:
        if player['account_id'] == user_infos[user_id].dota_id:
            current_player = player

    current_player_info = player_info(
        current_player['name'] or user_infos[user_id].name,
        current_player['hero_id'],
        current_player['level'],
        current_player['kills'],
        current_player['deaths'],
        current_player['assists'],
        current_player['last_hits'],
        current_player['denies'],
        [
            current_player['item_0'],
            current_player['item_1'],
            current_player['item_2'],
            current_player['item_3'],
            current_player['item_4'],
            current_player['item_5']
        ],
        current_player['item_neutral'],
        current_player['hero_damage'],
        current_player['hero_healing'],
        current_player['tower_damage'],
        current_player['net_worth'],
        current_player['gold_per_min'],
        current_player['xp_per_min'],
        current_player['isRadiant']
    )

    return match_info(
        last_match['match_id'],
        [current_player_info],
        last_match['start_time'],
        last_match['duration'],
        last_match['game_mode'],
        last_match['radiant_win'],
        last_match['dire_score'],
        last_match['radiant_score']
    )


async def get_last_match_results(user_id: str):
    last_match = await get_last_match_json(user_id)

    match_info = parse_last_match(last_match, user_id)

    settings = image_generator_settings()
    parser = dota_objects_parser('configs/heroes_ids.json', 'configs/item_ids.json', 'configs/game_mode.json')

    match_info_image = image_generator(settings).generate_last_match_statistics(parser, match_info)
    return image_to_bytes(match_info_image)


def parse_allies_statistics(user_id: str, statistics: json):
    user_dota_ids = [user_info.dota_id for user_info in user_infos.values()]
    filtered_statistics = list(filter(lambda stat: stat['account_id'] in user_dota_ids, statistics))

    allies = []
    for stat in filtered_statistics:
        allies.append(ally_info(stat['avatar'], stat['personaname'], stat['games'], stat['win']))

    stats = allies_statistics(user_infos[user_id].name, allies)

    settings = image_generator_settings(width=400, height=300)
    allies_statistics_image = image_generator(settings).generate_allies_statistics(stats)

    return image_to_bytes(allies_statistics_image)


async def get_allies_info_for_last_two_weeks(user_id: str):
    allies_statistics = await get_allies_statistics_json(user_id)
    return parse_allies_statistics(user_id, allies_statistics)
