from __future__ import annotations

import asyncio
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from sqlite3 import OperationalError, Cursor

from apps.core.database.query_constructor import QueryConstructor
from config.config import Udocan_Enable_Features_DB
from loader import logger

FILE_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent


class DataBaseSettings:

    def __init__(self):

        if not os.path.exists(Udocan_Enable_Features_DB):
            logger.error(f'Path {Udocan_Enable_Features_DB} is not exists!')

        self.db_file = Udocan_Enable_Features_DB
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.name: str = self.db_file.stem

    async def create_backup(self) -> str | None:
        """

        :return:
        """
        backup_file_path: str = f"C:\\backup\\{datetime.now().strftime('%d.%m.%Y')}\\"
        if not os.path.isdir(backup_file_path):
            os.makedirs(backup_file_path)

        query: str = f"vacuum into '{backup_file_path}backup_{datetime.now().strftime('%d.%m.%Y, %H.%M.%S')}_{self.name}.db'"

        try:
            with self.connection:
                result = self.cursor.execute(query)
                return self.name

        except (ValueError, sqlite3.OperationalError) as err:
            logger.error(f'Invalid query. {repr(err)}')
            return None

        finally:
            self.cursor.close()

    async def get_table_headers(self, table_name: str = None) -> list[str]:
        """Получение всех заголовков таблицы core_violations

        :return: list[ ... ]
        """
        if not table_name:
            return []

        with self.connection:
            result: list = self.cursor.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            clean_headers: list = [item[1] for item in result]
            return clean_headers

    async def get_all_tables_names(self) -> list:
        """Получение всех имен таблиц в БД

        :return:
        """
        with self.connection:
            result: list = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            return result

    async def get_data_list(self, query: str = None) -> list:
        """Получение данных из таблицы по запросу 'query'"""
        if not query:
            return []

        with self.connection:
            return self.cursor.execute(query).fetchall()

    async def get_data_list_without_query(self, table_name: str = None) -> list:
        """Получение данных из таблицы table_name"""
        try:
            with self.connection:
                query_kwargs: dict = {
                    "action": 'SELECT',
                    "subject": '*',
                }
                query: str = await QueryConstructor(None, table_name, **query_kwargs).prepare_data()
                result: list = self.cursor.execute(query).fetchall()
                if not result:
                    logger.error(f"no matches found {table_name} in DB "
                                 f"because .cursor.execute is none `table_name`: {table_name}")
                    return []
            return result

        except (ValueError, sqlite3.OperationalError) as err:
            logger.error(f'{repr(err)}')
            logger.error(f"Invalid query. {type(err).__name__} {err}")
            return []

        finally:
            self.cursor.close()

    async def update_column_value(self, query: str):
        """Обновление записи id в database

        :param query: str
        :return: result
        """
        with self.connection:
            result = self.cursor.execute(query)
        self.connection.commit()
        return result


class HSESettings:
    """Класс возврата сообщений на языке пользователя"""

    def __init__(self, user_id: int | str = None, *, cat=None, param: str = None, default: str | int | bool = 0,
                 now: bool = False):

        """Инициация класса сообщений STG для определения языка интерфейса пользователя

        :param user_id: int | str : id пользователя
        :param cat: str : optional : категория  в которой идет поиск сообщения
        :param param: str : optional : сообщение для поиска
        :param default: str : optional : сообщение по умолчанию
        :param now: bool : optional : требование немедленного возврата сообщения (блокирующая функция)
        """
        self.user_id: str | int = user_id
        self.__default_category: str = 'sett_main'
        self.category: str = f'sett_{cat}' if cat else self.__default_category
        self.param: str = param
        self.default = default

        if now: self.get_set()

    def __str__(self) -> str:
        """Возврат строкового значения"""
        return f'str: {self.get_set(self.param)}'

    async def __check_category_in_db(self, category: str = None) -> str:
        """Проверка наличия категории в базе данных

        :param category:
        :return:
        """

        all_tables: list = await DataBaseSettings().get_all_tables_names()

        if not all_tables:
            logger.error(f'Error get all_tables DB ! '
                         f'Set default_category: {self.__default_category}')
            return self.__default_category

        all_tables: list = [item[0] for item in all_tables if 'sett_' in item[0]]

        if category not in all_tables:
            logger.error(f'Error check {category = } in all_tables DB {all_tables}! '
                         f'Set default_category: {self.__default_category}')
            return self.__default_category

        return category

    async def __get_message_from_db(self, param: str = None, category: str = None) -> str:
        """Получение сообщение из БД на основе языка lang

        :param param: str сообщение для поиска в БД
        :param category: str категория для поиска в БД
        :return:
        """
        param: str = param if param else self.param
        table_name: str = category if category else self.category

        try:
            datas_list: list = await DataBaseSettings().get_data_list_without_query(table_name=table_name)

        except OperationalError as err:
            logger.error(f'The "{param}" {table_name = } is missing from the database! err: {repr(err)}')
            return f'def sett_ :{self.user_id} ::: {self.default}'

        if not datas_list:
            logger.error(f'Missing datas_list from the database. Set default value: {self.default}')
            return f'def sett_ :{self.user_id} ::: {self.default}'

        clean_headers: list = await DataBaseSettings().get_table_headers(table_name)
        list_dicts: list = [dict(zip(clean_headers, data_list)) for data_list in datas_list]

        try:
            fin_param: list = [item.get('value') for item in list_dicts if item.get('title') == param]

        except IndexError as err:
            logger.error(f'The "{param}" value is missing from the database. '
                         f'Set default value: {self.default} err: {repr(err)}')
            return f'def sett_ :{self.user_id} ::: {self.default}'

        if not fin_param:
            return ''

        if len(fin_param) >= 2:
            logger.warning(f'The "{param}" have 2 or more values\n used first values {fin_param[0] = }')
            return fin_param[0]

        return fin_param[-1]

    async def __get_all_items_from_table(self, param: str = None, category: str = None) -> list:
        """Получение сообщение из БД на основе языка lang

        :param param: str сообщение для поиска в БД
        :param category: str категория для поиска в БД
        :return:
        """
        param: str = param if param else self.param
        table_name: str = category if category else self.category

        try:
            datas_list: list = await DataBaseSettings().get_data_list_without_query(table_name=table_name)

        except OperationalError as err:
            logger.error(f'The "{param}" {table_name = } is missing from the database! err: {repr(err)}')
            return f'def sett_ :{self.user_id} ::: {self.default}'

        if not datas_list:
            logger.error(f'Missing datas_list from the database. Set default value: {self.default}')
            return f'def sett_ :{self.user_id} ::: {self.default}'

        clean_headers: list = await DataBaseSettings().get_table_headers(table_name)
        list_dicts: list = [dict(zip(clean_headers, data_list)) for data_list in datas_list]

        return list_dicts

    async def __get_set(self, param: str = None, category: str = None) -> int | bool:
        """Асинхронное получение сообщения из БД

        :param param: сообщение для поиска
        :param category: 'sett_{category}' - категория для поиска
        :return: str - текст сообщения
        """

        param: str = param if param else self.param
        category: str = category if category else self.category

        try:
            category: str = await self.__check_category_in_db(category=category)
            f_param: str = await self.__get_message_from_db(param=param, category=category)

            if not f_param:
                f_param = self.default

            return f_param

        except TypeError as err:
            logger.error(f'{repr(err)}')
            return self.default

    async def get_all_features(self, category: str = None) -> list:
        """
        :param category: 'sett_{category}' - категория для поиска
        :return:
        """

        category: str = f'sett_{category}' if category else self.category
        category: str = await self.__check_category_in_db(category=category)

        all_items: list = await self.__get_all_items_from_table(category=category)
        return all_items

    async def get_set_async(self, param: str = None, category: str = None) -> int | bool:
        """Асинхронное получение сообщения из БД

        :param param: сообщение для поиска
        :param category: 'sett_{category}' - категория для поиска
        :return:
        """
        param: str = param if param else self.param
        category: str = f'sett_{category}' if category else self.category

        f_param = await self.__get_set(param, category)
        return f_param

    def get_set(self, param: str = None, category: str = None) -> int | bool:
        """Получение языка из БД

        :param param: сообщение для поиска
        :param category: 'sett_{category}' категория для поиска
        :return:
        """

        param: str = param if param else self.param
        category: str = f'sett_{category}' if category else self.category

        f_param = asyncio.run(self.__get_set(param, category))
        return f_param


get_sett = HSESettings


async def test():
    """"""
    param: bool = await get_sett(cat='check', param='check_indefinite_normative').get_set_async()
    logger.info(f'{param = }')

    # message: str = str(await msg(hse_id, cat='msg_main', msge="acts_generated_successfully").g_mas())
    # logger.info(f'{message}')
    #
    # message: str = str(msg(hse_id, msg="acts_generated_successfully"))
    # logger.info(f'{hse_id = } ::: {message}')
    #
    # message: str = "acts_generated_successfully"
    # category: str = 'msg_main'
    # message = await msg(hse_id, msg=message, category=category).__get_message_from_db(lang=lang)
    # print(message)


if __name__ == '__main__':
    asyncio.run(test())

    param: bool = get_sett(cat='check', param='check_indefinite_normative').get_set()
    logger.info(f'no async {param = }')
