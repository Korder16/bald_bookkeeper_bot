import json
import io

from .dota_models import match_info, player_info
from ..image_generator import image_generator, image_generator_settings, dota_objects_parser
from .dota_api_client import get_last_match_json, get_allies_statistics_json
from ..user_infos import user_infos


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
    generator = image_generator(settings, parser)

    match_info_image = generator.generate_last_match_info_picture(match_info)
    img_byte_arr = io.BytesIO()
    match_info_image.save(img_byte_arr, format='webp')
    return img_byte_arr.getvalue()


def parse_allies_statistics(user_id: str, statistics: json):

    user_dota_ids = [user_info.dota_id for user_info in user_infos.values()]
    filtered_statistics = list(filter(lambda stat: stat['account_id'] in user_dota_ids, statistics))

    parsed_data = [f'{user_infos[user_id].name}, твой винрейт с кентами за последние 2 недели: ']
    for stat in filtered_statistics:
        nickname = stat['personaname']
        games = stat['games']
        wins = stat['win']
        loses = games - wins
        result = wins - loses
        result_str = f'{result}'
        if result > 0:
            result_str = f'+{result}'
        parsed_data.append(f'{nickname}: {games} игр ({result_str})')
    return '\n'.join(parsed_data)


async def get_allies_info_for_last_two_weeks(user_id: str):
    allies_statistics = await get_allies_statistics_json(user_id)
    return parse_allies_statistics(user_id, allies_statistics)