from dataclasses import dataclass

users_dota_id = {
    'islamtramov': 70040436,
    'TikhonovD': 92183733,
    'rash708': 46482901,
    'NSIbragim': 166583635,
    'misha1234555': 67777264,
    'NikoGasanov': 181487850
}

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
    items: list[int]
    neutral_item_id: int
    hero_damage: int
    hero_heal: int
    tower_damage: int
    net_worth: int
    gpm: int
    xpm: int
    team: bool

def make_player_info(nickname: str, hero_id: str, level: int, kills: int, deaths: int, assists: int, last_hits: int, denies: int, items: list[int], neutral_item_id: int, hero_damage: int, hero_heal:int, tower_damage: int, net_worth: int, gpm: int, xpm: int, team: bool):
    return player_info(nickname, hero_id, level, kills, deaths, assists, last_hits, denies, items, neutral_item_id, hero_damage, hero_heal, tower_damage, net_worth, gpm, xpm, team)

@dataclass
class match_info:
    id: int
    players: list[player_info]
    start_time: int
    duration: int
    game_mode_id: int
    radiant_win: bool
    dire_score: int
    radiant_score: int

def make_match_info(id: int, players: list[player_info], start_time: int, duration: int, game_mode_id: int, radiant_win: bool, dire_score: int, radiant_score: int):
    return match_info(id, players, start_time, duration, game_mode_id, radiant_win, dire_score, radiant_score)