import os.path
import sqlite3
import asyncio
import sys
from pathlib import Path
from pprint import pprint

from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.utils.secondary_functions.get_json_files import get_files
from loader import logger

BASE_DIR = Path(__file__).resolve()

ALL_CATEGORY_IN_DB: dict = {
    'main_category': 'core_maincategory',
    'location': 'core_location',
    'category': 'core_category',
    'violation_category': 'core_violationcategory',
    'general_contractor': 'core_generalcontractor',
    'act_required': 'core_actrequired',
    'incident_level': 'core_incidentlevel',
    'elimination_time': 'core_eliminationtime',
}


class DataBase:

    def __init__(self):

        self.db_file: str = os.path.join(BASE_DIR.parent.parent.parent.parent.parent, 'HSEViolationsDataBase.db')
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
            photo_full_name VARCHAR)
            """
        )

    def add_violation(self, *, violation: dict) -> bool:
        """Наполнение таблицы при первом запуске"""

        location = violation.get("location", None)
        if violation.get("year") == '2021' and violation.get("name") == 'Коршаков Алексей Сергеевич':
            location = 'Ст. Аминьевская'

        # location_id = self.get_location_id(location)
        # work_shift_id = self.get_work_shift_id(violation.get("work_shift", None))
        # main_category_id = self.get_main_category_id(violation.get('main_category', None))
        # general_contractor_id = self.get_general_contractor_id(violation.get('general_contractor', None))
        # category_id = self.get_category_id(violation.get('category', None))
        # act_required_id = self.get_act_required_id(violation.get('act_required', None))
        # elimination_time_id = self.get_elimination_time_id(violation.get('elimination_time', None))
        # incident_level_id = self.get_incident_level_id(violation.get('incident_level', None))
        # violation_category_id = self.get_violation_category_id(violation.get('violation_category', None))

        location_id = self.get_id(table='core_location', entry=location)
        work_shift_id = self.get_id(table='core_workshift', entry=violation.get("work_shift", None))

        general_contractor = violation.get("general_contractor", None)
        if general_contractor == 'МИП - Строй 1(?)':
            general_contractor = "МИП-Строй№1(?)"

        if general_contractor == "'Прочее'(?)":
            general_contractor = "Прочее"

        if general_contractor == "СиАрСиСи Рус(?)" or general_contractor == "'СиАрСиСи'(?)":
            general_contractor = "СиАрСиСи(?)"

        if general_contractor == "'МИП-С№1('ССМ')":
            general_contractor = "МИП-С№1('ССМ')"

        if general_contractor == "'СиАрСиСи'('РБТ')":
            general_contractor = "СиАрСиСи('РБТ')"

        if general_contractor == "'СиАрСиСи'('Стройком')":
            general_contractor = "СиАрСиСи('Стройком')"

        if general_contractor == "'МИП-Строй№1(?)":
            general_contractor = "МИП-Строй№1(?)"

        if general_contractor == "'МИП-С№1('Строй-монтаж2002')":
            general_contractor = "МИП-С№1('Строй-монтаж2002')"

        if general_contractor == "'МИП-С№1('ТрансЭнергоСнаб')":
            general_contractor = "МИП-С№1('ТрансЭнергоСнаб')"

        if general_contractor == "'ГорИнжПроект'(?)":
            general_contractor = "ГорИнжПроект(?)"

        if general_contractor == "'Прочее(?)" or general_contractor == "Прочее(?)":
            general_contractor = "Прочее"

        general_contractor_id = self.get_id(table='core_generalcontractor', entry=general_contractor)

        main_category = violation.get("main_category", None)
        if main_category == 'Промышленная безопасность_':
            main_category = 'Промышленная безопасность'

        main_category_id = self.get_id(table='core_maincategory', entry=main_category)

        category = violation.get("category", None)
        if category == 'Электробезопасность_':
            category = 'Электробезопасность'

        if category == 'Экология_':
            category = 'Отходы'

        if category == 'Работы на высоте_':
            category = 'Работы на высоте'

        category_id = self.get_id(table='core_category', entry=category, violation=violation)

        act_required_id = self.get_id(table='core_actrequired', entry=violation.get("act_required", None))
        description = violation.get('description', None)
        elimination_time_id = self.get_id(table='core_eliminationtime', entry=violation.get("elimination_time", None))
        incident_level_id = self.get_id(table='core_incidentlevel', entry=violation.get("incident_level", None))
        violation_category_id = self.get_id(table='core_violationcategory',
                                            entry=violation.get("violation_category", None))

        function = violation.get("function", None)
        name = violation.get("name", None)
        parent_id = violation.get("parent_id", None)
        violation_id = violation.get('violation_id', None)
        user_fullname = violation.get('user_fullname', None)
        report_folder_id = violation.get('report_folder_id', None)

        day = violation.get('day', None)
        month = violation.get('month', None)
        year = violation.get('year', None)

        title = violation.get('comment', None)
        comment = violation.get('comment', None)
        coordinates = violation.get('coordinates', None)
        latitude = violation.get('latitude', None)
        longitude = violation.get('longitude', None)
        json_folder_id = violation.get('json_folder_id', None)
        json_file_path = violation.get('json_file_path', None)
        json_full_name = violation.get('json_full_name', None)

        user_id = violation.get('user_id', None)
        file_id = violation.get('file_id', None)
        photo = f'/{user_id}/data_file/{file_id.split("___")[0]}/photo/report_data___{file_id}.jpg'
        json = f'/{user_id}/data_file/{file_id.split("___")[0]}/json/report_data___{file_id}.json'

        is_published = True
        is_finished = False

        photo_file_path = violation.get('photo_file_path', None)
        photo_folder_id = violation.get('photo_folder_id', None)
        photo_full_name = violation.get('photo_full_name', None)

        created_at = violation.get('data', None).split(':')
        created_at = '-'.join(created_at[::-1])
        updated_at = created_at

        try:
            with self.connection:
                is_add = self.cursor.execute(
                    "INSERT INTO `core_violations` (`location_id`,`work_shift_id` ,`function` ,`name` ,`parent_id`,"
                    "`violation_id`, `user_id`, `user_fullname`, `report_folder_id`, `file_id`, `is_published`,"
                    "`day`,`month`, `year`, `title`, `photo`,`created_at`,`updated_at`, `is_finished`,"
                    "`main_category_id`,`general_contractor_id`,`category_id`,`comment`,`act_required_id`,"
                    "`description`,`elimination_time_id`,`incident_level_id`,`violation_category_id`, `coordinates`,"
                    "`latitude`,`longitude`,`json_folder_id`,`json_file_path`,`json_full_name`,"
                    "`photo_file_path`,`photo_folder_id`,`photo_full_name`,`json`)"
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        location_id, work_shift_id, function, name, parent_id,
                        violation_id, user_id, user_fullname, report_folder_id, file_id, is_published,
                        day, month, year, title, photo, created_at, updated_at, is_finished,
                        main_category_id, general_contractor_id, category_id, comment, act_required_id,
                        description, elimination_time_id, incident_level_id, violation_category_id, coordinates,
                        latitude, longitude, json_folder_id, json_file_path, json_full_name,
                        photo_file_path, photo_folder_id, photo_full_name, json
                    )
                )
                if is_add:
                    return True
                return False

        except sqlite3.IntegrityError as err:
            pprint(f"sqlite3.IntegrityError {err}")

    def get_id(self, table, entry, violation=None) -> int:
        file_id = '000000'
        if violation:
            file_id = violation.get('file_id', None)

        if not entry:
            print(f"no entry {entry = }")
            return 0

        query = f"SELECT `id` FROM `{table}` WHERE `title` = ?"

        with self.connection:
            result = self.cursor.execute(query, (entry,)).fetchall()
            if not result:
                print(f"no matches found {entry = } in {table} because .cursor.execute is none file_id: {file_id}")
                # sys.exit()

            entry_id = 0
            for row in result:
                entry_id = int(row[0])
                return entry_id

            if entry_id == 0:
                print(f"no matches found {entry = } in {table} because entry_id file_id: {file_id}")
                # sys.exit()

    def get_table_info(self):
        with self.connection:
            result = self.cursor.execute("PRAGMA table_info('core_violations')").fetchall()
            return result

    def get_violation(self, violation_file_id: str) -> list:
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `core_violations` WHERE `file_id` = ?',
                                         (violation_file_id,)).fetchall()
            return result

    def violation_exists(self, file_id: int):
        """Проверка наличия violation_id в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `core_violations` WHERE `file_id` = ?',
                                         (file_id,)).fetchall()
            return bool(len(result))

    def delete_violation(self, file_id: int):
        #  Удаление записи
        with self.connection:
            return self.cursor.execute("DELETE FROM `core_violations` WHERE `file_id` = ?", (file_id,))

    def get_info_violations(self, file_id: int):
        # получение информации по юзеру
        with self.connection:
            return self.cursor.execute("SELECT * FROM `core_violations` WHERE `file_id` = ?",
                                       (file_id,)).fetchone()

    def count_violations(self):
        # вывод кол-ва юзеров
        with self.connection:
            return self.cursor.execute('SELECT COUNT(*) FROM `core_violations`').fetchone()

    def all_violations(self):
        # вывод кол-ва юзеров
        with self.connection:
            return self.cursor.execute('SELECT * FROM `core_violations`').fetchall()

    def get_data_list(self, query: str = None) -> list:
        if not query:
            return []

        with self.connection:
            return self.cursor.execute(query).fetchall()


async def write_json(violation):
    """Запись в файл"""
    if not os.path.isfile(violation['json_full_name']):
        print(f"FileNotFoundError {violation['json_full_name']} ")

        date_violation = violation['file_id'].split('___')[0]

        violation['json_full_name'] = \
            f"C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot\\user_data\\373084462\\data_file" \
            f"\\{date_violation}\\json\\report_data___{violation['file_id']}.json"
        violation['photo_full_name'] = \
            f"C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot\\user_data\\373084462\\data_file" \
            f"\\{date_violation}\\photo\\report_data___{violation['file_id']}.jpg"

        await write_json_file(data=violation, name=violation['json_full_name'])
        return

    await write_json_file(data=violation, name=violation['json_full_name'])


async def get_entry(violation, query, user_data_json_file) -> int:
    table = ALL_CATEGORY_IN_DB[query]

    if not violation.get(query):
        violation[query] = user_data_json_file.get("name_location")
        # await write_json(violation=violation)

    entry = violation.get(query, None)
    query_id = DataBase().get_id(table=table, entry=entry)
    return query_id


async def run(*, params: dict = None):
    # if not os.path.exists(params['file_path']):
    #     print(f"ERROR file: {params['file_path']} don't exists")
    #     exit(0)
    #
    # if not os.path.exists(params['user_file']):
    #     print(f"ERROR file: {params['user_file']} don't exists")
    #     exit(0)
    #
    # if not os.path.isfile(params['user_file']):
    #     print(f"ERROR file: {params['user_file']} not a file")
    #     exit(0)

    json_file_list = await get_files(params['file_path'], endswith=".json")

    error_counter: int = 0
    comment_counter: int = 0
    act_required_counter: int = 0
    elimination_time_counter: int = 0
    general_contractor_counter: int = 0
    incident_level_counter: int = 0

    for counter, violation_file in enumerate(json_file_list, start=1):

        violation = await read_json_file(file=violation_file)
        user_data_json_file = await read_json_file(file=params['user_file'])
        file_id = violation.get('file_id')

        if not violation.get("work_shift"):
            violation["work_shift"] = user_data_json_file.get("work_shift")
            await write_json(violation=violation)

        if not violation.get("function"):
            violation["function"] = user_data_json_file.get("function")
            await write_json(violation=violation)

        if not violation.get("name"):
            violation["name"] = user_data_json_file.get("name")
            await write_json(violation=violation)

        if not violation.get("parent_id"):
            violation["parent_id"] = user_data_json_file.get("parent_id")
            await write_json(violation=violation)

        if not violation.get('general_contractor'):
            print(f"ERROR file: {file_id} don't get 'general_contractor' parameter")
            error_counter += 1
            general_contractor_counter += 1

            os.remove(violation_file)
            print(f"file: {violation_file} is remove")
            continue

        if not violation.get('elimination_time'):
            print(f"ERROR file: {file_id} don't get 'elimination_time' parameter")
            error_counter += 1
            elimination_time_counter += 1
            violation['elimination_time'] = '1 день'
            await write_json(violation=violation)
            continue

        if not violation.get('incident_level'):
            print(f"ERROR file: {file_id} don't get 'incident_level' parameter")
            error_counter += 1
            incident_level_counter += 1
            violation['incident_level'] = 'Без последствий'
            await write_json(violation=violation)
            continue

        if not violation.get('act_required'):
            print(f"ERROR file: {file_id} don't get 'act_required' parameter")
            error_counter += 1
            act_required_counter += 1
            os.remove(violation_file)
            print(f"file: {violation_file} is remove")
            continue

        if not violation.get('comment'):
            print(f"ERROR file: {file_id} don't get 'comment' parameter")
            error_counter += 1
            comment_counter += 1
            continue

        if not DataBase().violation_exists(file_id):
            # location_id = await get_entry(violation=violation, query="location",
            #                               user_data_json_file=user_data_json_file)
            # print(f'{location_id = }')

            is_add = DataBase().add_violation(violation=violation)
            if is_add:
                logger.info(f"{counter} file {violation.get('file_id')} add in db {DataBase().db_file}")

    print(f"errors {error_counter} in {len(json_file_list)} items")
    print(f"general_contractor_counter {general_contractor_counter} in {error_counter} items")
    print(f"elimination_time_counter {elimination_time_counter} in {error_counter} items")
    print(f"act_required_counter {act_required_counter} in {error_counter} items")
    print(f"incident_level_counter {incident_level_counter} in {error_counter} items")
    print(f"comment_counter {comment_counter} in {error_counter} items")


if __name__ == '__main__':
    user_chat_id = '373084462'
    params: dict = {
        'all_files': True,
        'file_path': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{user_chat_id}/data_file/",
        'user_file': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{user_chat_id}/{user_chat_id}.json"
    }

    asyncio.run(run(params=params))
    print(f'count_violations {DataBase().count_violations()}')

    # work_shift_id = DataBase().get_work_shift_id(violation.get("work_shift", None))
    # main_category_id = DataBase().get_main_category_id(violation.get('main_category', None))
    # general_contractor_id = DataBase().get_general_contractor_id(violation.get('general_contractor', None))
    # category_id = DataBase().get_category_id(violation.get('category', None))
    # act_required_id = DataBase().get_act_required_id(violation.get('act_required', None))
    # elimination_time_id = DataBase().get_elimination_time_id(violation.get('elimination_time', None))
    # incident_level_id = DataBase().get_incident_level_id(violation.get('incident_level', None))
    # violation_category_id = DataBase().get_violation_category_id(violation.get('violation_category', None))
