from PIL import Image, ImageDraw, ImageFont
from .dota.dota_models import match_info, allies_statistics, ally_info
import json
from datetime import datetime
from time import strftime, gmtime
from dataclasses import dataclass
from random import choice


def num_to_k(num: int):
    if num > 1000:
        return round(num / 1000, 1)
    else:
        return num


@dataclass
class fonts:
    normal = ImageFont.truetype('fonts/LiberationMono-BoldItalic.ttf', size=16, encoding="unic")
    title = ImageFont.truetype('fonts/LiberationMono-BoldItalic.ttf', size=20, encoding="unic")


@dataclass
class text_colors:
    white: str = 'white'
    grey: str = 'grey'
    gold: str = '#FBB829'
    yellow: str = '#F2CC67'
    light_blue: str = '#30BFD2'
    green: str = '#92A525'
    red: str = '#C23C2A'


@dataclass
class image_generator_settings:
    text_color = text_colors()
    font = fonts()
    width: int = 1230
    height: int = 200


class dota_objects_parser:
    def __init__(self, heroes_ids_filename: str, items_ids_filename: str, game_mode_filename: str) -> None:
        with open(heroes_ids_filename) as f:
            self.__hero_icons_data = json.load(f)

        with open(items_ids_filename) as f:
            self.__item_icons_data = json.load(f)

        with open(game_mode_filename) as f:
            self.__game_mode_data = json.load(f)

    def get_hero_icon_path_by_id(self, hero_id: int):
        return f'media/hero_icons/{self.__hero_icons_data[str(hero_id)]}.webp'

    def get_item_icon_path_by_item_id(self, item_id: int):
        item_name = self.__item_icons_data[str(item_id)]
        if 'recipe' in item_name:
            return 'media/item_icons/recipe.webp'
        else:
            return f'media/item_icons/{item_name}.webp'

    def get_game_mode_by_id(self, game_mode_id: int):
        return self.__game_mode_data[str(game_mode_id)]


class statistics_image_generator:

    def __init__(self, settings: image_generator_settings, parser: dota_objects_parser) -> None:
        self.__settings = settings
        self.__parser = parser

    def get_match_results(self, radiant_win: bool, team: bool):
        victory_messages = ['разнёс бомжей', 'засолил', '2ez', 'в сола']
        defeat_messages = ['отлетел очередняра', 'заруинили', 'за тупость']

        if (radiant_win and team) or (not radiant_win and not team):
            result_message = choice(victory_messages)
            return result_message, self.__settings.text_color.green
        else:
            result_message = choice(defeat_messages)
            return result_message, self.__settings.text_color.red

    def get_team(self, team: bool):
        if team:
            return 'СВЕТА', self.__settings.text_color.green
        else:
            return 'ТЬМЫ', self.__settings.text_color.red

    def generate_match_info_template(self):
        img = Image.new('RGBA', (self.__settings.width, self.__settings.height), (28, 36, 45))
        idraw = ImageDraw.Draw(img)

        title_text_height = 5
        text_height = 130
        idraw.text((10, title_text_height), 'Матч', self.__settings.text_color.white, self.__settings.font.title)
        idraw.text((480, title_text_height + 20), 'ТИП ЛОББИ', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((610, title_text_height + 20), 'РЕЖИМ ИГРЫ', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((720, title_text_height + 20), 'РЕГИОН', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((800, title_text_height + 20), 'ДЛИТЕЛЬНОСТЬ', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((1000, title_text_height + 20), 'ДАТА', self.__settings.text_color.grey, self.__settings.font.normal)

        idraw.text((10, text_height), 'Герой', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((80, text_height), 'Игрок', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((380, text_height), ' У', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((405, text_height), ' С', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((430, text_height), ' П', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((460, text_height), '   ОЦ', self.__settings.text_color.gold, self.__settings.font.normal)
        idraw.text((520, text_height), '  Д', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((560, text_height), 'НО', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((595, text_height), 'З/М', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((635, text_height), 'О/М', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((687, text_height), 'Урон', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((750, text_height), 'Лечение', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((835, text_height), 'Постр', self.__settings.text_color.white, self.__settings.font.normal)

        idraw.text((945, text_height), 'Предметы', self.__settings.text_color.white, self.__settings.font.normal)

        img.save('media/template.webp')

    def generate_last_match_info_picture(self, m_info: match_info):
        self.generate_match_info_template()
        template_image = Image.open('media/template.webp')
        idraw = ImageDraw.Draw(template_image)

        title_text_height = 5
        idraw.text((65, title_text_height), f'{m_info.id}', self.__settings.text_color.white, self.__settings.font.title)
        idraw.text((480, title_text_height), 'Рейтинговый', self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((610, title_text_height), self.__parser.get_game_mode_by_id(m_info.game_mode_id), self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((720, title_text_height), 'Россия', self.__settings.text_color.white, self.__settings.font.normal)

        duration = strftime('%H:%M:%S', gmtime(m_info.duration)).lstrip('0:')
        idraw.text((800, title_text_height), duration, self.__settings.text_color.white, self.__settings.font.normal)

        pretty_start_time = datetime.fromtimestamp(m_info.start_time, tz=None).strftime("%d.%m.%Y, %H:%M:%S")
        idraw.text((940, title_text_height), pretty_start_time, self.__settings.text_color.white, self.__settings.font.normal)

        result, result_color = self.get_match_results(m_info.radiant_win, m_info.players[0].team)
        idraw.text((540, title_text_height + 50), result, result_color, self.__settings.font.title)
        idraw.text((530, title_text_height + 80), f'{m_info.radiant_score}', self.__settings.text_color.green, self.__settings.font.title)
        idraw.text((590, title_text_height + 80), duration, self.__settings.text_color.white, self.__settings.font.title)
        idraw.text((670, title_text_height + 80), f'{m_info.dire_score}', self.__settings.text_color.red, self.__settings.font.title)

        team, team_color = self.get_team(m_info.players[0].team)

        text_height = 160
        idraw.text((10, text_height - 60), f'СИЛЫ {team}', team_color, self.__settings.font.title)

        for player in m_info.players:
            hero_icon = Image.open(self.__parser.get_hero_icon_path_by_id(player.hero_id)).resize((43, 24))
            idraw.text((80, text_height), player.nickname, self.__settings.text_color.white, self.__settings.font.normal)
            idraw.text((380, text_height), f'{player.kills}', self.__settings.text_color.white, self.__settings.font.normal)
            idraw.text((405, text_height), f'{player.deaths}', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((430, text_height), f'{player.assists}', self.__settings.text_color.white, self.__settings.font.normal)
            idraw.text((460, text_height), f'{num_to_k(player.net_worth)}K', self.__settings.text_color.gold, self.__settings.font.normal)
            idraw.text((520, text_height), f'{player.last_hits}', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((560, text_height), f'{player.denies}', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((595, text_height), f'{num_to_k(player.gpm)}', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((635, text_height), f'{num_to_k(player.xpm)}', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((677, text_height), f'{num_to_k(player.hero_damage)}K', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((770, text_height), f'{num_to_k(player.hero_heal)}K', self.__settings.text_color.grey, self.__settings.font.normal)
            idraw.text((835, text_height), f'{num_to_k(player.tower_damage)}', self.__settings.text_color.grey, self.__settings.font.normal)

            item_indent = 0
            for item_id in player.items:
                if item_id != 0:
                    item_icon = Image.open(self.__parser.get_item_icon_path_by_item_id(item_id)).resize((38, 28))
                    template_image.paste(item_icon, (940 + item_indent, text_height))
                item_indent += 40

            if player.neutral_item_id != 0:
                neutral_item_icon = Image.open(self.__parser.get_item_icon_path_by_item_id(player.neutral_item_id)).resize((38, 28))
                template_image.paste(neutral_item_icon, (950 + item_indent, text_height))

        template_image.paste(hero_icon, (10, text_height))
        return template_image


class allies_statistics_image_generator:

    def __init__(self, settings: image_generator_settings) -> None:
        self.__settings = settings

    def generate_player_info(self, idraw: ImageDraw, nickname: str):
        idraw.text((10, 25), f'{nickname}, твой винрейт с кентами', self.__settings.text_color.white, self.__settings.font.title)

    def generate_player_info_without_allies(self, idraw: ImageDraw, nickname: str):
        idraw.text((10, 25), f'{nickname}, сори, кентов нет', self.__settings.text_color.white, self.__settings.font.title)

    def generate_header(self, idraw: ImageDraw):
        start_y = 25
        idraw.text((10, start_y + 40), 'ИМЯ', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((10, start_y + 60), 'СОЮЗНИКА', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((150, start_y + 40), 'ЧИСЛО', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((150, start_y + 60), 'ИГР', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((230, start_y + 40), 'ПОБ', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((230, start_y + 60), 'ПОР', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((310, start_y + 40), 'ДОЛЯ', self.__settings.text_color.grey, self.__settings.font.normal)
        idraw.text((310, start_y + 60), 'ПОБЕД', self.__settings.text_color.grey, self.__settings.font.normal)

    def generate_ally_info(self, idraw: ImageDraw, ally: ally_info, text_height: int):
        nickname_x = 10
        loses = ally.total_games - ally.wins
        result = ally.wins - loses

        idraw.text((nickname_x, text_height), ally.nickname, self.__settings.text_color.white, self.__settings.font.normal)
        idraw.text((nickname_x + 140, text_height), f'{ally.total_games}', self.__settings.text_color.white, self.__settings.font.normal)
        if result >= 0:
            idraw.text((nickname_x + 220, text_height), f'{result}', self.__settings.text_color.green, self.__settings.font.normal)
        else:
            idraw.text((nickname_x + 220, text_height), f'{result}', self.__settings.text_color.red, self.__settings.font.normal)

        winrate = (ally.wins / ally.total_games) * 100
        idraw.text((nickname_x + 300, text_height), f'{winrate:.1f}%', self.__settings.text_color.white, self.__settings.font.normal)

    def generate_allies_info(self, idraw: ImageDraw, statistics: allies_statistics):
        text_height = 125

        for ally in statistics.allies:
            self.generate_ally_info(idraw, ally, text_height)
            text_height += 35

    def generate_allies_statistics_image(self, statistics: allies_statistics):
        if len(statistics.allies) > 0:
            img = Image.new('RGBA', (self.__settings.width, 140 + 35 * len(statistics.allies)), (28, 36, 45))
            idraw = ImageDraw.Draw(img)

            self.generate_player_info(idraw, statistics.nickname)
            self.generate_header(idraw)
            self.generate_allies_info(idraw, statistics)
        else:
            img = Image.new('RGBA', (self.__settings.width, 70), (28, 36, 45))
            idraw = ImageDraw.Draw(img)

            self.generate_player_info_without_allies(idraw, statistics.nickname)
        return img


class image_generator:

    def __init__(self, settings: image_generator_settings) -> None:
        self.__settings = settings

    def generate_allies_statistics(self, statistics: allies_statistics):
        generator = allies_statistics_image_generator(self.__settings)
        return generator.generate_allies_statistics_image(statistics)
