from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
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


@dataclass_json
@dataclass
class match_info:
    id: int
    radiant_team: List[player_info]
    dire_team: List[player_info]
    start_time: int
    duration: int
    game_mode_id: int
    radiant_win: bool
    dire_score: int
    radiant_score: int
