from dataclasses import dataclass
import json

user_infos = {}

@dataclass
class user_info:
    name: str
    dota_id: int
    stop_working_hour: int

def parse_user_config():
    with open('configs/user_infos.json', 'r') as f:
        user_infos_json = json.load(f)
        for user_id, user_value in user_infos_json.items():
            user_infos[user_id] = user_info(user_value['name'], user_value['dota_id'], user_value['stop_working_hour'])
