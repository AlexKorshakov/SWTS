import os
import sqlite3
from os import makedirs

from pandas import DataFrame
from pprint import pprint

from apps.core.utils.json_worker.read_json_file import read_json_file
from apps.core.utils.json_worker.writer_json_file import write_json_file
from apps.core.utils.secondary_functions.get_json_files import get_files
from config.config import DATA_BASE_DIR

from loader import logger


class DataBase:

    def __init__(self):

        self.db_file: str = DATA_BASE_DIR
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def add_violation(self, *, violation: dict) -> bool:
        """Добавление записей в database

        :param violation: dict с данными для внесения
        """

        file_id = violation.get('file_id', None)

        if not file_id:
            logger.error(f'not found file_id!!!')
            return False

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
            name='main_location'
        )
        sub_location_id = self.get_id(
            table='core_sublocation',
            entry=violation.get("sub_location", None),
            file_id=file_id,
            name='sub_location'
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
        # hse_id = self.get_id(
        #     table='core_hseuser',
        #     entry=violation.get("hse_id", None),
        #     file_id=file_id,
        #     name='hse_id'
        # )

        hse_id = violation.get("hse_id", None)

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

        week_id = violation.get("week", None)
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
                    " 'hse_id', 'function', 'name', 'user_id', 'location_id', 'act_number', 'agreed_id', "
                    " 'violation_id', "
                    " 'main_location_id', 'sub_location_id', 'work_shift_id', 'created_at', 'updated_at', "
                    " 'main_category_id', 'status_id', 'finished_id', 'is_published', 'comment', 'description', "
                    " 'general_contractor_id',  'category_id',  'normative_documents_id',  'violation_category_id', "
                    " 'incident_level_id',  'act_required_id',  'elimination_time_id',  'file_id', "
                    " 'photo', 'title', 'day', 'month', 'year','week_id', 'quarter', 'day_of_year', "
                    " 'json_folder_id', 'parent_id', 'photo_folder_id', "
                    " 'report_folder_id', 'coordinates', 'latitude', 'longitude', 'json_file_path', 'json_full_name', "
                    " 'photo_file_path', 'photo_full_name', 'user_fullname', 'json' "
                    ")"
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                    "?,?,?)",
                    (
                        hse_id, function, name, user_id, location_id, act_number, agreed_id, violation_id,
                        main_location_id, sub_location_id, work_shift_id, created_at, updated_at,
                        main_category_id, status_id, finished_id, is_published, comment, description,
                        general_contractor_id, category_id, normative_documents_id, violation_category_id,
                        incident_level_id, act_required_id, elimination_time_id, file_id, photo, title,
                        day, month, year, week_id, quarter, day_of_year,
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

    def get_dict_data_from_table_from_id(self, table_name: str, id: int, query: str = None) -> dict:

        if not query:
            query: str = f'SELECT * ' \
                         f'FROM {table_name} ' \
                         f'WHERE `id` = {id} '

        headers: list = [item[1] for item in self.get_table_headers(table_name)]
        values: list = self.get_data_list(query=query)
        clean_values: list = values[0]

        return dict((header, item_value) for header, item_value in zip(headers, clean_values))

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

    def set_act_value(self, act_data_dict: DataFrame, act_number: int, act_date: str):
        """Добавление записи в database core_actsprescriptions

        """
        act_number = str(act_number)
        act_date = str(act_date)
        act_row_count = len(act_data_dict.index)

        act_location_id = int(act_data_dict.location_id.unique()[0])
        act_week = int(act_data_dict.week_id.unique()[0])
        act_month = int(act_data_dict.month.unique()[0])
        act_quarter = int(act_data_dict.quarter.unique()[0])
        act_year = int(act_data_dict.year.unique()[0])
        act_hse_id = int(act_data_dict.hse_id.unique()[0])

        act_status_id = int(act_data_dict.status_id.unique()[0])
        act_general_contractor_id = int(act_data_dict.general_contractor_id.unique()[0])

        try:
            with self.connection:
                is_add = self.cursor.execute(
                    "INSERT INTO `core_actsprescriptions` ("
                    "`act_number`, `act_date`, `act_hse_id`, `act_row_count`, `act_location_id`,`act_week`,`act_month`,"
                    "`act_quarter`, `act_year`, `act_status_id`, `act_general_contractor_id` "
                    ")"
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
                    (
                        act_number, act_date, act_hse_id, act_row_count, act_location_id, act_week, act_month,
                        act_quarter, act_year, act_status_id, act_general_contractor_id
                    )
                )
                if is_add:
                    logger.info(f"act {act_number} date {act_date} complete successfully for act_hse_id {act_hse_id}")
                    return True

                logger.error(f"ERROR!!! act {act_number} date {act_date} error for act_hse_id {act_hse_id}")
                return False

        except sqlite3.IntegrityError as err:
            logger.error(f"ERROR!!! act {act_number} date {act_date} error for act_hse_id {act_hse_id}")
            logger.error(f"sqlite3.IntegrityError {err}")
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

        # normalize_violation = await normalize_violation_data(violation=violation)
        normalize_violation = violation

        if not DataBase().violation_exists(violation.get('file_id')):
            is_add = DataBase().add_violation(violation=normalize_violation)
            if is_add:
                logger.debug(f"{counter} file {violation.get('file_id')} add in db")

            len_err += error_counter
    print(f"errors {len_err} in {len(json_file_list)} items")


async def data_violation_completion(violation_file: str, params: dict) -> tuple[int, dict]:
    """
    :param

    """
    error_counter: int = 0
    # comment_counter: int = 0
    # act_required_counter: int = 0
    # elimination_time_counter: int = 0
    # general_contractor_counter: int = 0
    # incident_level_counter: int = 0

    violation = await read_json_file(file=violation_file)
    user_data_json_file = await read_json_file(file=params['user_file'])
    file_id = violation.get('file_id')

    if not violation.get("work_shift"):
        violation["work_shift"] = user_data_json_file.get("work_shift")

    if not violation.get("function"):
        violation["function"] = user_data_json_file.get("function")

    if not violation.get("name"):
        violation["name"] = user_data_json_file.get("name")

    if not violation.get("parent_id"):
        violation["parent_id"] = user_data_json_file.get("parent_id")

    if not violation.get("location"):
        violation["location"] = user_data_json_file.get("name_location")

    if not violation.get("status"):
        print(f"ERROR file: {file_id} don't get 'status' parameter")
        error_counter += 1
        violation["status"] = 'Завершено'

    if not violation.get("violation_id"):
        print(f"ERROR file: {file_id} don't get 'violation_id' parameter")
        error_counter += 1
        violation["violation_id"] = violation['file_id'].split('___')[-1]

    if not violation.get("json_folder_id"):
        print(f"ERROR file: {file_id} don't get 'json_folder_id' parameter")
        error_counter += 1
        violation["json_folder_id"] = '0'

    if not violation.get('general_contractor'):
        print(f"ERROR file: {file_id} don't get 'general_contractor' parameter")
        error_counter += 1

        # general_contractor_counter += 1
        # os.remove(violation_file)
        # print(f"file: {violation_file} is remove")

    if not violation.get('elimination_time'):
        print(f"ERROR file: {file_id} don't get 'elimination_time' parameter")
        error_counter += 1
        # elimination_time_counter += 1
        violation['elimination_time'] = '1 день'

    if not violation.get('incident_level'):
        print(f"ERROR file: {file_id} don't get 'incident_level' parameter")
        error_counter += 1
        # incident_level_counter += 1
        violation['incident_level'] = 'Без последствий'
        await write_json(violation=violation)

    if not violation.get('act_required'):
        print(f"ERROR file: {file_id} don't get 'act_required' parameter")
        error_counter += 1
        # act_required_counter += 1
        violation['act_required'] = 'Не требуется*'

    if not violation.get('comment'):
        print(f"ERROR file: {file_id} don't get 'comment' parameter")
        error_counter += 1
        # comment_counter += 1

    # print(f"general_contractor_counter {general_contractor_counter} in {error_counter} items")
    # print(f"elimination_time_counter {elimination_time_counter} in {error_counter} items")
    # print(f"act_required_counter {act_required_counter} in {error_counter} items")
    # print(f"incident_level_counter {incident_level_counter} in {error_counter} items")
    # print(f"comment_counter {comment_counter} in {error_counter} items")

    await write_json(violation=violation)

    return error_counter, violation


async def write_json(violation):
    """Запись в файл"""
    if not os.path.isfile(violation['json_full_name']):
        print(f"FileNotFoundError {violation['json_full_name']} ")

    date_violation = violation['file_id'].split('___')[0]

    violation['json_full_name'] = \
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file" \
        f"\\{date_violation}\\json\\report_data___{violation['file_id']}.json"

    await create_file_path(
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file"
        f"\\{date_violation}\\json\\"
    )
    violation['photo_full_name'] = \
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file" \
        f"\\{date_violation}\\photo\\report_data___{violation['file_id']}.jpg"

    await create_file_path(
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file"
        f"\\{date_violation}\\photo\\"
    )

    await write_json_file(data=violation, name=violation['json_full_name'])


async def create_file_path(path: str):
    """Проверка и создание путей папок и файлов
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        # logger.info(f"user_path{path} is directory")
        try:
            makedirs(path)
        except Exception as err:
            logger.info(f"makedirs err {repr(err)}")
