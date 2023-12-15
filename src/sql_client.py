import asyncpg
from os import getenv


class bald_bookeeper_bot_db_client:

    async def __connect(self):
        return await asyncpg.connect(
            database=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST"),
            port=getenv("DB_PORT")
        )

    async def __select_one(self, sql_query: str):
        connection = await self.__connect()

        row = await connection.fetchrow(sql_query)
        await connection.close()
        return row

    async def get_username_by_tg_id(self, id: int) -> str:
        row = await self.__select_one(f'select u.name from usernames u, telegram_accounts t where t.telegram_id = {id} and t.id = u.id')
        return row['name']

    async def get_stop_working_hour_by_tg_id(self, id: int) -> int:
        sql_query = f'select w.stop_working_hour from works w, telegram_accounts t where t.telegram_id = {id} and w.id = t.id'

        row = await self.__select_one(sql_query)
        stop_working_hour = row['stop_working_hour']

        if stop_working_hour == -1:
            return 0
        else:
            return stop_working_hour

    async def get_dota_id_by_tg_id(self, id: int) -> str:
        row = await self.__select_one(f'select d.dota_account_id from dota_accounts d, telegram_accounts t where t.telegram_id = {id} and t.id = d.id')
        return row['dota_account_id']

    async def get_all_dota_ids(self) -> list:
        sql_query = 'select dota_account_id from dota_accounts'

        with self.__connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return [dota_id[0] for dota_id in cursor.fetchall()]

    async def get_username_by_dota_id(self, id: int) -> str:
        row = await self.__select_one(f'select u.name from dota_accounts d, usernames u where d.dota_account_id = {id} and d.id = u.id')
        return row['name']

    async def get_last_match_id(self, dota_account_id: int) -> int:
        row = await self.__select_one(f'select last_match_id from dota_accounts where dota_account_id = {dota_account_id};')
        return row['last_match_id']

    async def update_last_match_id(self, dota_account_id: int, last_match_id: int):
        sql_query = f'update dota_accounts set last_match_id = {last_match_id} where dota_account_id = {dota_account_id};'

        connection = await self.__connect()
        await connection.execute(sql_query)
        await connection.close()

    async def is_match_image_file_id_exists(self, match_id: int) -> bool:
        row = await self.__select_one(f'select count(1) from match_statistics_images where match_id = {match_id}')
        return row['count']

    async def get_match_image_file_id(self, match_id: int) -> str:
        row = await self.__select_one(f'select tg_image_file_id from match_statistics_images where match_id = {match_id}')
        return row['tg_image_file_id']

    async def insert_match_image_file_id(self, match_id: int, image_file_id: str):
        sql_query = f"insert into match_statistics_images (match_id, tg_image_file_id) values ({match_id}, '{image_file_id}')"

        connection = await self.__connect()
        await connection.execute(sql_query)
        await connection.close()

    async def __get_tg_file_id_by_media_name(self, media_name: str) -> str:
        row = await self.__select_one(f"select tg_file_id from tg_media where media_name = '{media_name}';")
        return row['tg_file_id']

    async def get_rock_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('rock')

    async def get_rama_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('rama')

    async def get_squirrel_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('squirrel')

    async def get_miracle_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('miracle')

    async def get_golovach_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('golovach')

    async def get_clown_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('clown')

    async def get_medusa_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('medusa')

    async def get_marathon_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('marathon')

    async def get_legion_commander_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('legion_commander')
    
    async def get_shame_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('shame')

    async def get_guys_file_id(self) -> str:
        return await self.__get_tg_file_id_by_media_name('guys')

    async def get_random_dura_file_id(self) -> str:
        row = await self.__select_one("select tg_file_id from tg_media where media_name = 'dura' order by RANDOM() limit 1;")
        return row['tg_file_id']

    async def get_random_ibragym_file_id(self) -> str:
        row = await self.__select_one("select tg_file_id from tg_media where media_name = 'ibragym' order by RANDOM() limit 1;")
        return row['tg_file_id']
