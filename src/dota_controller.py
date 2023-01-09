import json
import io

from .dota_models import user_dota_ids, match_info, player_info
from .image_generator import image_generator, image_generator_settings, dota_objects_parser
from .dota_api_client import get_last_match_json, get_allies_statistics_json

def parse_last_match(last_match: json, username: str):
    players = last_match['players']

    for player in players:
        if player['account_id'] == user_dota_ids[username]:
            current_player = player

    current_player_info = player_info(
        current_player['name'] or username,
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
    parser = dota_objects_parser('heroes_ids.json', 'item_ids.json', 'game_mode.json')
    generator = image_generator(settings, parser)

    match_info_image = generator.generate_last_match_info_picture(match_info)
    img_byte_arr = io.BytesIO()
    match_info_image.save(img_byte_arr, format='webp')
    return img_byte_arr.getvalue()


def parse_allies_statistics(user_id: str, statistics: json):
    
    filtered_statistics = list(filter(lambda stat: stat['account_id'] in user_dota_ids.values(), statistics))
    
    parsed_data = [f'Кенты {user_id}: ']
    for stat in filtered_statistics:
        nickname = stat['personaname']
        games = stat['games']
        wins = stat['win']
        loses = games - wins
        parsed_data.append(f'{nickname}: {games} игр ({wins - loses})')
    return '\n'.join(parsed_data)
    

async def get_allies_statistics(user_id: str):
    allies_statistics = await get_allies_statistics_json(user_id)
    return parse_allies_statistics(user_id, allies_statistics)
