from dataclasses import dataclass
from typing import List
import json

with open('user_infos.json', 'r') as f:
    user_infos = json.load(f)
    user_dota_ids = {}
    for user_id, user_value in user_infos.items():
        user_dota_ids[user_id] = user_value['dota_id']


@dataclass
class player_info:
    nickname: str
    hero_id: str
    level: int
    kills: int
    deaths: int
    assists: int
    last_hits: int
    denies: int
    items: List[int]
    neutral_item_id: int
    hero_damage: int
    hero_heal: int
    tower_damage: int
    net_worth: int
    gpm: int
    xpm: int
    team: bool

@dataclass
class match_info:
    id: int
    players: List[player_info]
    start_time: int
    duration: int
    game_mode_id: int
    radiant_win: bool
    dire_score: int
    radiant_score: int
