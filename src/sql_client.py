import psycopg2
from os import getenv


class bald_bookeeper_bot_db_client:

    def __connect(self):
        return psycopg2.connect(
            database=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST"),
            port=getenv("DB_PORT")
        )

    def __select_one(self, sql_query: str):
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return cursor.fetchone()[0]

    def __select_all(self, sql_query: str):
        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return [elem[0] for elem in cursor.fetchall()]

    def get_username_by_tg_id(self, id: int) -> str:
        return self.__select_one(f'select u.name from usernames u, telegram_accounts t where t.telegram_id = {id} and t.id = u.id')

    def get_stop_working_hour_by_tg_id(self, id: int) -> int:
        sql_query = f'select w.stop_working_hour from works w, telegram_accounts t where t.telegram_id = {id} and w.id = t.id'

        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                stop_work_hour = cursor.fetchone()
                if stop_work_hour == -1:
                    return 0
                else:
                    return stop_work_hour[0]

    def get_dota_id_by_tg_id(self, id: int) -> str:
        return self.__select_one(f'select d.dota_account_id from dota_accounts d, telegram_accounts t where t.telegram_id = {id} and t.id = d.id')

    def get_all_dota_ids(self) -> list:
        sql_query = 'select dota_account_id from dota_accounts'

        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return [dota_id[0] for dota_id in cursor.fetchall()]

    def get_username_by_dota_id(self, id: int) -> str:
        return self.__select_one(f'select u.name from dota_accounts d, usernames u where d.dota_account_id = {id} and d.id = u.id')

    def get_last_match_id(self, dota_account_id: int) -> int:
        return self.__select_one(f'select last_match_id from dota_accounts where dota_account_id = {dota_account_id};')

    def update_last_match_id(self, dota_account_id: int, last_match_id: int):
        sql_query = f'update dota_accounts set last_match_id = {last_match_id} where dota_account_id = {dota_account_id};'

        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

    def is_match_image_file_id_exists(self, match_id: int) -> bool:
        return self.__select_one(f'select count(1) from match_statistics_images where match_id = {match_id}')

    def get_match_image_file_id(self, match_id: int) -> str:
        return self.__select_one(f'select tg_image_file_id from match_statistics_images where match_id = {match_id}')

    def insert_match_image_file_id(self, match_id: int, image_file_id: str):
        sql_query = f"insert into match_statistics_images (match_id, tg_image_file_id) values ({match_id}, '{image_file_id}')"

        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

    def __get_tg_file_id_by_media_name(self, media_name: str) -> str:
        return self.__select_one(f"select tg_file_id from tg_media where media_name = '{media_name}';")

    def get_rock_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('rock')

    def get_rama_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('rama')

    def get_squirrel_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('squirrel')

    def get_miracle_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('miracle')

    def get_golovach_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('golovach')

    def get_clown_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('clown')

    def get_medusa_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('medusa')

    def get_marathon_file_id(self) -> str:
        return self.__get_tg_file_id_by_media_name('marathon')

    def get_random_dura_file_id(self) -> str:
        return self.__select_one("select tg_file_id from tg_media where media_name = 'dura' order by RANDOM() limit 1;")

    def get_random_ibragym_file_id(self) -> str:
        return self.__select_one("select tg_file_id from tg_media where media_name = 'ibragym' order by RANDOM() limit 1;")
