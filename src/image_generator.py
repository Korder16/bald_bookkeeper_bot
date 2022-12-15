from PIL import Image, ImageDraw, ImageFont
from .dota_models import match_info
import json
from datetime import datetime
from time import strftime, gmtime


WHITE_TEXT_COLOR = 'white'
GREY_TEXT_COLOR = 'grey'
GOLD_TEXT_COLOR = '#FBB829'
YELLOW_TEXT_COLOR = '#F2CC67'
LIGHT_BLUE_TEXT_COLOR = '#30BFD2'
GREEN_TEXT_COLOR = '#92A525'
RED_TEXT_COLOR = '#C23C2A'

NORMAL_FONT = ImageFont.truetype('/usr/share/fonts/liberation-mono/LiberationMono-BoldItalic.ttf', size=16, encoding="unic")
TITLE_FONT = ImageFont.truetype('/usr/share/fonts/liberation-mono/LiberationMono-BoldItalic.ttf', size=20, encoding="unic")

# TODO: refactor this block
with open('heroes_ids.json') as f:
    hero_icons_data = json.load(f)

with open('item_ids.json') as f:
    item_icons_data = json.load(f)

with open('game_mode.json') as f:
    game_mode_data = json.load(f)


def get_hero_icon_path_by_id(hero_id: int):
    return f'media/hero_icons/{hero_icons_data[str(hero_id)]}.webp'


def get_item_icon_path_by_item_id(item_id: int):
    item_name = item_icons_data[str(item_id)]
    if 'recipe' in item_name:
        return 'media/item_icons/recipe.webp'
    else:
        return f'media/item_icons/{item_name}.webp'


def num_to_k(num: int):
    if num > 1000:
        return round(num / 1000, 1)
    else:
        return num


def get_game_mode_by_id(game_mode_id: int):
    return game_mode_data[str(game_mode_id)]


def get_match_results(radiant_win: bool):
    if radiant_win:
        return 'ПОБЕДА СИЛ СВЕТА', GREEN_TEXT_COLOR
    else:
        return 'ПОБЕДА СИЛ ТЬМЫ', RED_TEXT_COLOR


def get_team(team: bool):
    if team:
        return 'СВЕТА', GREEN_TEXT_COLOR
    else:
        return 'ТЬМЫ', RED_TEXT_COLOR


def generate_match_info_template():
    img = Image.new('RGBA', (1230, 200), (28, 36, 45))
    idraw = ImageDraw.Draw(img)

    title_text_height = 5
    text_height = 130
    idraw.text((10, title_text_height), 'Матч', WHITE_TEXT_COLOR, TITLE_FONT)
    idraw.text((480, title_text_height + 20), 'ТИП ЛОББИ', GREY_TEXT_COLOR, NORMAL_FONT)
    idraw.text((610, title_text_height + 20), 'РЕЖИМ ИГРЫ', GREY_TEXT_COLOR, NORMAL_FONT)
    idraw.text((720, title_text_height + 20), 'РЕГИОН', GREY_TEXT_COLOR, NORMAL_FONT)
    idraw.text((800, title_text_height + 20), 'ДЛИТЕЛЬНОСТЬ', GREY_TEXT_COLOR, NORMAL_FONT)
    idraw.text((1000, title_text_height + 20), 'ДАТА', GREY_TEXT_COLOR, NORMAL_FONT)

    idraw.text((10, text_height), 'Герой', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((80, text_height), 'Игрок', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((380, text_height), ' У', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((405, text_height), ' С', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((430, text_height), ' П', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((460, text_height), '   ОЦ', GOLD_TEXT_COLOR, NORMAL_FONT)
    idraw.text((520, text_height), '  Д', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((560, text_height), 'НО', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((595, text_height), 'З/М', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((635, text_height), 'О/М', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((687, text_height), 'Урон', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((750, text_height), 'Лечение', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((835, text_height), 'Постр', WHITE_TEXT_COLOR, NORMAL_FONT)

    idraw.text((945, text_height), 'Предметы', WHITE_TEXT_COLOR, NORMAL_FONT)

    img.save('template.webp')


def generate_last_match_info_picture(m_info: match_info):
    generate_match_info_template()
    template_image = Image.open('template.webp')
    idraw = ImageDraw.Draw(template_image)

    title_text_height = 5
    idraw.text((65, title_text_height), f'{m_info.id}', WHITE_TEXT_COLOR, TITLE_FONT)
    idraw.text((480, title_text_height), 'Рейтинговый', WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((610, title_text_height), get_game_mode_by_id(m_info.game_mode_id), WHITE_TEXT_COLOR, NORMAL_FONT)
    idraw.text((720, title_text_height), 'Россия', WHITE_TEXT_COLOR, NORMAL_FONT)

    duration = strftime('%H:%M:%S', gmtime(m_info.duration)).lstrip('0:')
    idraw.text((800, title_text_height), duration, WHITE_TEXT_COLOR, NORMAL_FONT)

    pretty_start_time = datetime.fromtimestamp(m_info.start_time, tz=None).strftime("%d.%m.%Y, %H:%M:%S")
    idraw.text((940, title_text_height), pretty_start_time, WHITE_TEXT_COLOR, NORMAL_FONT)

    result, result_color = get_match_results(m_info.radiant_win)
    idraw.text((520, title_text_height + 50), result, result_color, TITLE_FONT)
    idraw.text((530, title_text_height + 80), f'{m_info.radiant_score}', GREEN_TEXT_COLOR, TITLE_FONT)
    idraw.text((590, title_text_height + 80), duration, WHITE_TEXT_COLOR, TITLE_FONT)
    idraw.text((670, title_text_height + 80), f'{m_info.dire_score}', RED_TEXT_COLOR, TITLE_FONT)

    team, team_color = get_team(m_info.players[0].team)

    text_height = 160
    idraw.text((10, text_height - 60), f'СИЛЫ {team}', team_color, TITLE_FONT)

    for player in m_info.players:
        hero_icon = Image.open(get_hero_icon_path_by_id(player.hero_id)).resize((43, 24))
        idraw.text((80, text_height), player.nickname, WHITE_TEXT_COLOR, NORMAL_FONT)
        idraw.text((380, text_height), f'{player.kills}', WHITE_TEXT_COLOR, NORMAL_FONT)
        idraw.text((405, text_height), f'{player.deaths}', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((430, text_height), f'{player.assists}', WHITE_TEXT_COLOR, NORMAL_FONT)
        idraw.text((460, text_height), f'{num_to_k(player.net_worth)}K', GOLD_TEXT_COLOR, NORMAL_FONT)
        idraw.text((520, text_height), f'{player.last_hits}', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((560, text_height), f'{player.denies}', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((595, text_height), f'{num_to_k(player.gpm)}', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((635, text_height), f'{num_to_k(player.xpm)}', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((677, text_height), f'{num_to_k(player.hero_damage)}K', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((770, text_height), f'{num_to_k(player.hero_heal)}K', GREY_TEXT_COLOR, NORMAL_FONT)
        idraw.text((835, text_height), f'{num_to_k(player.tower_damage)}', GREY_TEXT_COLOR, NORMAL_FONT)

        item_indent = 0
        for item_id in player.items:
            if item_id != 0:
                item_icon = Image.open(get_item_icon_path_by_item_id(item_id)).resize((38, 28))
                template_image.paste(item_icon, (940 + item_indent, text_height))
            item_indent += 40

        if player.neutral_item_id != 0:
            neutral_item_icon = Image.open(get_item_icon_path_by_item_id(player.neutral_item_id)).resize((38, 28))
            template_image.paste(neutral_item_icon, (950 + item_indent, text_height))

    template_image.paste(hero_icon, (10, text_height))
    return template_image
