import os.path
import sqlite3
from pandas import DataFrame
from pathlib import Path
from pprint import pprint
from random import randint

from apps.core.bot.database.db_utils import normalize_violation_data, write_json, data_violation_completion
from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.secondary_functions.get_json_files import get_files
from config.web.settings import DB_NAME
from loader import logger

BASE_DIR = Path(__file__).resolve()

CATEGORY_ID_TRANSFORM: dict = {
    'main_category': {
        'item': 'main_category',
        'column': 'main_category_id',
        'table': 'core_maincategory',
        'description': 'Основная категория'
    },
    'location': {
        'item': 'location',
        'column': 'location_id',
        'table': 'core_location',
        'description': 'Закреплённый участок'
    },
    'main_location': {
        'item': 'main_location',
        'column': 'main_location_id',
        'table': 'core_mainlocation',
        'description': 'Площадка'
    },
    'sub_location': {
        'item': 'sub_location',
        'column': 'sub_location_id',
        'table': 'core_sublocation',
        'description': 'Под площадка / участок'
    },
    'category': {
        'item': 'category',
        'column': 'category_id',
        'table': 'core_category',
        'description': 'Категория'
    },
    'normative_documents': {
        'item': 'normative_documents',
        'column': 'normative_documents_id',
        'table': 'core_normativedocuments',
        'description': 'Под Категория'
    },
    'violation_category': {
        'item': 'violation_category',
        'column': 'violation_category_id',
        'table': 'core_violationcategory',
        'description': 'Категория нарушения'
    },
    'general_contractor': {
        'item': 'general_contractor',
        'column': 'general_contractor_id',
        'table': 'core_generalcontractor',
        'description': 'Подрядчик',
        'json_file_name': 'GENERAL_CONTRACTORS'
    },
    'act_required': {
        'item': 'act_required',
        'column': 'act_required_id',
        'table': 'core_actrequired',
        'description': 'Требуется оформление Акта-предписания?'
    },
    'incident_level': {
        'item': 'incident_level',
        'column': 'incident_level_id',
        'table': 'core_incidentlevel',
        'description': 'Уровень происшествия'
    },
    'elimination_time': {
        'item': 'elimination_time',
        'column': 'elimination_time_id',
        'table': 'core_eliminationtime',
        'description': 'Время на устранение'
    },
    'status': {
        'item': 'status',
        'column': 'status_id',
        'table': 'core_status',
        'description': 'Статус'
    },
    'work_shift': {
        'item': 'work_shift',
        'column': 'work_shift_id',
        'table': 'core_workshift',
        'description': 'Смена'
    },
}


class DataBase:

    def __init__(self):

        self.db_file: str = os.path.join(BASE_DIR.parent.parent.parent.parent.parent, DB_NAME)
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """Создание таблицы violation"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            location VARCHAR NOT NULL,
            work_shift VARCHAR,
            function VARCHAR,
            name VARCHAR NOT NULL,
            parent_id VARCHAR NOT NULL,
            
            violation_id INTEGER,
            user_id INTEGER NOT NULL,
            user_fullname VARCHAR (100),
            report_folder_id VARCHAR (100),
            file_id VARCHAR NOT NULL,
            data VARCHAR NOT NULL,
            day VARCHAR (10) NOT NULL,
            month VARCHAR (10) NOT NULL,
            year VARCHAR (10) NOT NULL,
            now VARCHAR (100) NOT NULL,
            main_category VARCHAR NOT NULL,
            general_contractor VARCHAR NOT NULL,
            category VARCHAR NOT NULL,
            normative_documents VARCHAR,
            comment VARCHAR NOT NULL,
            act_required VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            elimination_time VARCHAR NOT NULL,
            incident_level VARCHAR NOT NULL,
            violation_category VARCHAR NOT NULL,
            coordinates VARCHAR,
            latitude FLOAT DEFAULT (0),
            longitude FLOAT DEFAULT (0),
            json_folder_id VARCHAR (100) NOT NULL,
            json_file_path VARCHAR,
            json_full_name VARCHAR,
            photo_file_path VARCHAR,
            photo_folder_id VARCHAR (100) NOT NULL,
            photo_full_name VARCHAR
            )
            """
        )

    def add_violation(self, *, violation: dict) -> bool:
        """Добавление записей в database

        :param violation: dict с данными для внесения
        """

        file_id = violation.get('file_id', None)

        location_id = self.get_id(
            table='core_location',
            entry=violation.get("location", None),
            file_id=file_id,
            name='location'
        )
        main_location_id = self.get_id(
            table='core_mainlocation',
            entry=violation.get("main_location", None),
            file_id=file_id,
            name='location'
        )
        sub_location_id = self.get_id(
            table='core_sublocation',
            entry=violation.get("sub_location", None),
            file_id=file_id,
            name='location'
        )
        work_shift_id = self.get_id(
            table='core_workshift',
            entry=violation.get("work_shift", None),
            file_id=file_id,
            name='work_shift'
        )
        general_contractor_id = self.get_id(
            table='core_generalcontractor',
            entry=violation.get("general_contractor", None),
            file_id=file_id,
            name='general_contractor'
        )
        main_category_id = self.get_id(
            table='core_maincategory',
            entry=violation.get("main_category", None),
            file_id=file_id,
            name='main_category'
        )
        category_id = self.get_id(
            table='core_category',
            entry=violation.get("category", None),
            file_id=file_id,
            name='category'
        )
        normative_documents_id = self.get_id(
            table='core_normativedocuments',
            entry=violation.get("normative_documents", None),
            file_id=file_id,
            name='normative_documents'
        )
        act_required_id = self.get_id(
            table='core_actrequired',
            entry=violation.get("act_required", None),
            file_id=file_id,
            name='act_required'
        )
        elimination_time_id = self.get_id(
            table='core_eliminationtime',
            entry=violation.get("elimination_time", None),
            file_id=file_id,
            name='elimination_time'
        )
        incident_level_id = self.get_id(
            table='core_incidentlevel',
            entry=violation.get("incident_level", None),
            file_id=file_id,
            name='incident_level'
        )
        violation_category_id = self.get_id(
            table='core_violationcategory',
            entry=violation.get("violation_category", None),
            file_id=file_id,
            name='violation_category'
        )
        status_id = self.get_id(
            table='core_status',
            entry=violation.get("status", None),
            file_id=file_id,
            name='status'
        )
        finished_id = self.get_id(
            table='core_finished',
            entry=violation.get("finished", None),
            file_id=file_id,
            name='finished'
        )
        agreed_id = self.get_id(
            table='core_agreed',
            entry=violation.get("agreed", None),
            file_id=file_id,
            name='agreed'
        )

        # TODO: check act_number
        act_number = ''

        if status_id == 1:
            finished_id = 1

        description = violation.get('description', None)

        is_published = True

        function = violation.get("function", None)
        name = violation.get("name", None)
        parent_id = violation.get("parent_id", None)
        violation_id = violation.get('violation_id', None)
        user_fullname = violation.get('user_fullname', None)
        report_folder_id = violation.get('report_folder_id', None)

        day = violation.get('day', None)
        month = violation.get('month', None)
        year = violation.get('year', None)

        week = violation.get("week", None)
        quarter = violation.get("quarter", None)
        day_of_year = violation.get("day_of_year", None)

        title = violation.get('comment', None)
        comment = violation.get('comment', None)

        coordinates = violation.get('coordinates', None)
        latitude = violation.get('latitude', None)
        longitude = violation.get('longitude', None)

        json_folder_id = violation.get('json_folder_id', None)
        json_file_path = violation.get('json_file_path', None)
        json_full_name = violation.get('json_full_name', None)

        user_id = violation.get('user_id', None)

        photo = f'/{user_id}/data_file/{file_id.split("___")[0]}/photo/report_data___{file_id}.jpg'
        json = f'/{user_id}/data_file/{file_id.split("___")[0]}/json/report_data___{file_id}.json'

        photo_file_path = violation.get('photo_file_path', None)
        photo_folder_id = violation.get('photo_folder_id', None)
        photo_full_name = violation.get('photo_full_name', None)

        created_at = violation.get('file_id', None).split('___')[0].split('.')
        created_at = '-'.join(created_at[::-1])

        updated_at = created_at

        try:
            with self.connection:
                is_add = self.cursor.execute(
                    "INSERT INTO `core_violations` ("
                    " 'function', 'name', 'user_id', 'location_id', 'act_number', 'agreed_id', 'violation_id', "
                    " 'main_location_id', 'sub_location_id', 'work_shift_id', 'created_at', 'updated_at', "
                    " 'main_category_id', 'status_id', 'finished_id', 'is_published', 'comment', 'description', "
                    " 'general_contractor_id',  'category_id',  'normative_documents_id',  'violation_category_id', "
                    " 'incident_level_id',  'act_required_id',  'elimination_time_id',  'file_id', "
                    " 'photo', 'title', 'day', 'month', 'year','week', 'quarter', 'day_of_year', "
                    " 'json_folder_id', 'parent_id', 'photo_folder_id', "
                    " 'report_folder_id', 'coordinates', 'latitude', 'longitude', 'json_file_path', 'json_full_name', "
                    " 'photo_file_path', 'photo_full_name', 'user_fullname', 'json' "
                    ")"
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                    "?,?,?)",
                    (
                        function, name, user_id, location_id, act_number, agreed_id, violation_id,
                        main_location_id, sub_location_id, work_shift_id, created_at, updated_at,
                        main_category_id, status_id, finished_id, is_published, comment, description,
                        general_contractor_id, category_id, normative_documents_id, violation_category_id,
                        incident_level_id, act_required_id, elimination_time_id, file_id, photo, title,
                        day, month, year, week, quarter, day_of_year,
                        json_folder_id, parent_id, photo_folder_id, report_folder_id,
                        coordinates, latitude, longitude,
                        json_file_path, json_full_name, photo_file_path, photo_full_name, user_fullname, json
                    )
                )
                if is_add:
                    return True

                logger.error(f'error in file {file_id}')
                return False

        except sqlite3.IntegrityError as err:
            pprint(f"sqlite3.IntegrityError {err}")
            return False

    def get_id(self, table: str, entry, file_id: str = None, name=None) -> int:
        """Получение id записи по значению title из соответствующий таблицы table"""

        if not entry:
            print(f" def get_id: no entry {entry = } {file_id = } entry name {name}")
            return 0

        query = f"SELECT `id` " \
                f"FROM `{table}` " \
                f"WHERE `title` = ?"

        with self.connection:
            result = self.cursor.execute(query, (entry,)).fetchall()
            if not result:
                logger.error(
                    f"no matches found {entry = } in {table} in title "
                    f"because .cursor.execute is none file_id: {file_id}")
                query = f"SELECT `id` " \
                        f"FROM `{table}` " \
                        f"WHERE `short_title` = ?"
                result = self.cursor.execute(query, (entry,)).fetchall()
                if not result:
                    logger.error(
                        f"no matches found {entry = } in {table} in short_title "
                        f"because .cursor.execute is none file_id: {file_id}")

            entry_id = 0
            for row in result:
                entry_id = int(row[0])
                return entry_id

            if entry_id == 0:
                print(f"no matches found {entry = } in {table} because entry_id file_id: {file_id}")

    def get_id_violation(self, file_id: str = None) -> int:
        """Получение id записи по значению file_id из таблицы core_violations"""

        query = "SELECT `id` FROM `core_violations` WHERE `file_id` = ?"
        with self.connection:
            result = self.cursor.execute(query, (file_id,)).fetchall()
            if not result:
                logger.error(f"no matches found {file_id} in core_violations because "
                             f".cursor.execute is none")
                return 0

            return result[0][0]

    def get_table_headers(self, table_name: str = None) -> list[str]:
        """Получение всех заголовков таблицы core_violations

        :return: list[ ... ]
        """

        if table_name:
            query: str = f"PRAGMA table_info('{table_name}')"
            with self.connection:
                result = self.cursor.execute(query).fetchall()
                return result

        with self.connection:
            result = self.cursor.execute("PRAGMA table_info('core_violations')").fetchall()
            return result

    def get_single_violation(self, file_id: str) -> list:
        """Получение записи по id

        :param file_id: file_id из таблицы core_violations
        :return: list[ ... ] or []
        """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `core_violations` WHERE `file_id` = ?',
                                         (file_id,)).fetchall()
            return result

    def violation_exists(self, file_id: int):
        """Проверка наличия violation_id в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `core_violations` WHERE `file_id` = ?',
                                         (file_id,)).fetchall()
            return bool(len(result))

    def delete_single_violation(self, file_id: int):
        """Удаление записи"""
        with self.connection:
            return self.cursor.execute("DELETE FROM `core_violations` WHERE `file_id` = ?", (file_id,))

    def get_info_violations(self, file_id: int):
        """Получение информации"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `core_violations` WHERE `file_id` = ?",
                                       (file_id,)).fetchone()

    def count_violations(self):
        """Вывод кол-ва записей из core_violations
        """
        with self.connection:
            return self.cursor.execute('SELECT COUNT(*) FROM `core_violations`').fetchone()

    def get_count_items(self, table_name):
        """Вывод кол-ва записей из core_violations
        """
        with self.connection:
            return self.cursor.execute(f'SELECT COUNT(*) FROM `{table_name}`').fetchone()

    def all_violations(self):
        """Вывод кол-ва юзеров"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM `core_violations`').fetchall()

    def get_data_list(self, query: str = None) -> list:
        """Получение данных из таблицы по запросу 'query'"""
        if not query:
            return []

        with self.connection:
            return self.cursor.execute(query).fetchall()

    def get_dict_data_from_table_from_id(self, table_name: str, id: int) -> dict:

        query: str = f'SELECT * ' \
                     f'FROM {table_name} ' \
                     f'WHERE `id` = {id} '

        headers: list = [item[1] for item in self.get_table_headers(table_name)]
        values: list = self.get_data_list(query=query)[0]

        return dict((header, item_value) for header, item_value in zip(headers, values))

    def update_column_value(self, column_name: str, value: str, id: str):
        """Обновление записи id в database

        :param id: id записи
        :param value:  значение для записи в столбец
        :param column_name: столбец
        """

        query: str = f"UPDATE `core_violations` SET {column_name} = ? WHERE `id` = ?"
        logger.debug(f'{column_name = } {value = }')
        with self.connection:
            self.cursor.execute(query, (value, id,))
        self.connection.commit()

    def set_act_value(self, act_data_dict: DataFrame, act_number, act_date):
        """Добавление записи в database core_actsprescriptions

        """
        act_number = str(act_number)
        act_date = str(act_date)
        act_row_count = len(act_data_dict.index)

        act_location_id = act_data_dict.location_id.unique()[0]
        act_week = act_data_dict.week.unique()
        act_month = act_data_dict.month.unique()
        act_quarter = act_data_dict.quarter.unique()
        act_year = act_data_dict.year.unique()

        try:
            with self.connection:
                is_add = self.cursor.execute(
                    "INSERT INTO `core_actsprescriptions` ("
                    "`act_number`, `act_date`, `act_row_count`, `act_location_id`,`act_week`,`act_month`,"
                    "`act_quarter`, `act_year` "
                    ")"
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        act_number, act_date, act_row_count, act_location_id, act_week, act_month, act_quarter,
                        act_year
                    )
                )
                if is_add:
                    return True

                # logger.error(f'error in file {file_id}')
                return False

        except sqlite3.IntegrityError as err:
            pprint(f"sqlite3.IntegrityError {err}")
            return False

    def get_full_title(self, table_name: str, short_title: str):
        """Получение полного имени из короткого

        :param short_title: данные для поиска (короткое имя)
        :param table_name:имя таблицы для запроса
        """

        query: str = f'SELECT * FROM {table_name}'

        datas_query: list = self.get_data_list(query=query)
        full_title = [item[1] for item in datas_query if item[2] == short_title][0]

        return full_title

    def get_max_max_number(self) -> int:
        """Получение максимального номера акта из Database `core_actsprescriptions`
        """
        query: str = 'SELECT `act_number` FROM `core_actsprescriptions`'
        datas_query: list = self.get_data_list(query=query)
        act_max_number = max([data_item[0] for data_item in datas_query])

        return act_max_number


# async def get_entry(violation, query, user_data_json_file) -> int:
#     table = ALL_CATEGORY_IN_TABLES_DB[query]
#
#     if not violation.get(query):
#         violation[query] = user_data_json_file.get("name_location")
#         # await write_json(violation=violation)
#
#     entry = violation.get(query, None)
#     query_id = DataBase().get_id(table=table, entry=entry)
#     return query_id


async def upload_from_local(*, params: dict = None):
    """Проверка валидация и загрузка файлов в database из local storage

    :param params: dict с путями к файлам для загрузки

    params{
        'file_path': '...',
        'user_file': '...'
        }
    """

    json_file_list = await get_files(params['file_path'], endswith=".json")

    len_err = 0
    for counter, violation_file in enumerate(json_file_list, start=1):

        error_counter, violation = await data_violation_completion(violation_file=violation_file, params=params)

        normalize_violation = await normalize_violation_data(violation=violation)

        if not DataBase().violation_exists(violation.get('file_id')):
            is_add = DataBase().add_violation(violation=normalize_violation)
            if is_add:
                logger.debug(f"{counter} file {violation.get('file_id')} add in db")

            len_err += error_counter
    print(f"errors {len_err} in {len(json_file_list)} items")


async def sync_files(*, params: dict = None):
    """Синхронизация файлов между локальным хранилищем media и облаком google_drive """

    # await sync_local_to_google_drive()

    await google_drive_to_local()


async def google_drive_to_local():
    """Синхронизация google_drive -> media"""
    pass
