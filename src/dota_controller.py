import json
import io

from .dota_models import users_dota_id, make_match_info, make_player_info
from .image_generator import generate_last_match_info_picture
from .dota_io_client import get_last_match_json, update_player_matches


def parse_last_match(last_match: json, username: str):
    players = last_match['players']

    for player in players:
        if player['account_id'] == users_dota_id[username]:
            current_player = player

    current_player_info = make_player_info(
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

    return make_match_info(
        last_match['match_id'],
        [current_player_info],
        last_match['start_time'],
        last_match['duration'],
        last_match['game_mode'],
        last_match['radiant_win'],
        last_match['dire_score'],
        last_match['radiant_score']
    )


async def get_last_match_results(username: str):
    await update_player_matches(username)
    last_match = await get_last_match_json(username)

    match_info = parse_last_match(last_match, username)

    match_info_image = generate_last_match_info_picture(match_info)
    img_byte_arr = io.BytesIO()
    match_info_image.save(img_byte_arr, format='webp')
    return img_byte_arr.getvalue()
