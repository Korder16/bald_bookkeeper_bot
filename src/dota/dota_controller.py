import json

from .dota_models import match_info, player_info
from .opendota_api_client import opendota_api_client
from ..user_infos import user_infos


def parse_last_match(last_match: json):
    players = last_match['players']

    player_team = 'radiant'

    match_players = []
    for player in players:
        player_name = 'бомж'
        for user_info in user_infos.values():
            if player['account_id'] == user_info.dota_id:
                player_name = user_info.name

                if not player['isRadiant']:
                    player_team = 'dire'

        match_players.append(player_info(
            player_name,
            player['hero_id'],
            player['level'],
            player['kills'],
            player['deaths'],
            player['assists'],
            player['last_hits'],
            player['denies'],
            [
                player['item_0'],
                player['item_1'],
                player['item_2'],
                player['item_3'],
                player['item_4'],
                player['item_5']
            ],
            player['item_neutral'],
            player['hero_damage'],
            player['hero_healing'],
            player['tower_damage'],
            player['net_worth'],
            player['gold_per_min'],
            player['xp_per_min'],
            player['isRadiant']
        ))

    radiant_team = [player for player in match_players if player.team is True]
    dire_team = [player for player in match_players if player.team is False]

    return (match_info(
        last_match['match_id'],
        radiant_team,
        dire_team,
        last_match['start_time'],
        last_match['duration'],
        last_match['game_mode'],
        last_match['radiant_win'],
        last_match['dire_score'],
        last_match['radiant_score']
    ),
        (player_team == 'radiant' and last_match['radiant_win']) or (player_team == 'dire' and not last_match['radiant_win']))


async def get_last_match_results(user_id: str):
    client = opendota_api_client()
    last_match = await client.get_last_match_json(user_id)

    match_info, is_win = parse_last_match(last_match)
    return match_info.to_json(), is_win


async def get_allies_info_for_last_two_weeks(user_id: str):
    client = opendota_api_client()
    return await client.get_allies_statistics_json(user_id)
