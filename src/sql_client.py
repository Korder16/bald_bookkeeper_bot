import psycopg2
from os import getenv


# def connect_db():
#     try:
#         return psycopg2.connect(
#             database=getenv("DB_NAME"),
#             user=getenv("DB_USER"),
#             password=getenv("DB_PASSWORD"),
#             host=getenv("DB_HOST")
#         )
#     except:
#         print('Cannot connect to db')


class bald_bookeeper_bot_db_client:

    def __init__(self) -> None:
        self.__connection = psycopg2.connect(
            database=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST")
        )

    def __del__(self):
        self.__connection.close()

    def get_username_by_tg_id(self, id: int) -> str:
        sql_query = f'select u.name from users u, telegram_accounts t where t.telegram_id = {id} and t.id = u.id'

        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return cursor.fetchone()[0]

    def get_stop_working_hour_by_tg_id(self, id: int):
        sql_query = f'select w.stop_working_hour from works w, telegram_accounts t where t.telegram_id = {id} and w.id = t.id'

        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                stop_work_hour = cursor.fetchone()
                if stop_work_hour is None:
                    return 0
                else:
                    return stop_work_hour[0]

    def get_dota_id_by_tg_id(self, id: int) -> str:
        sql_query = f'select d.dota_account_id from dota_accounts d, telegram_accounts t where t.telegram_id = {id} and t.id = d.id'

        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return cursor.fetchone()[0]

    def get_all_dota_ids(self) -> list:
        sql_query = 'select dota_account_id from dota_accounts'

        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return [dota_id[0] for dota_id in cursor.fetchall()]

    def get_username_by_dota_id(self, id: int) -> str:
        sql_query = f'select u.name from dota_accounts d, users u where d.dota_account_id = {id} and d.id = u.id'

        with self.__connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                return cursor.fetchone()[0]
