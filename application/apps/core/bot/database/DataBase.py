import os.path
import sqlite3
import asyncio
import sys
from pathlib import Path

from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.utils.secondary_functions.get_json_files import get_files

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

    def add_violation(self, *, violation: dict):
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
        main_category_id = self.get_id(table='core_maincategory', entry=violation.get("main_category", None))
        general_contractor_id = self.get_id(table='core_generalcontractor',
                                            entry=violation.get("general_contractor", None))
        category_id = self.get_id(table='core_category', entry=violation.get("category", None))
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
        is_published = True
        is_finished = False

        photo_file_path = violation.get('photo_file_path', None)
        photo_folder_id = violation.get('photo_folder_id', None)
        photo_full_name = violation.get('photo_full_name', None)

        created_at = violation.get('data', None).split(':')
        created_at = '-'.join(created_at[::-1])
        updated_at = created_at

        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `core_violations` (`location_id`,`work_shift_id` ,`function` ,`name` ,`parent_id`,"
                "`violation_id`, `user_id`, `user_fullname`, `report_folder_id`, `file_id`, `is_published`,"
                "`day`,`month`, `year`, `title`, `photo`,`created_at`,`updated_at`, `is_finished`,"
                "`main_category_id`,`general_contractor_id`,`category_id`,`comment`,`act_required_id`,"
                "`description`,`elimination_time_id`,`incident_level_id`,`violation_category_id`, `coordinates`,"
                "`latitude`,`longitude`,`json_folder_id`,`json_file_path`,`json_full_name`,"
                "`photo_file_path`,`photo_folder_id`,`photo_full_name`)"
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    location_id, work_shift_id, function, name, parent_id,
                    violation_id, user_id, user_fullname, report_folder_id, file_id, is_published,
                    day, month, year, title, photo, created_at, updated_at, is_finished,
                    main_category_id, general_contractor_id, category_id, comment, act_required_id,
                    description, elimination_time_id, incident_level_id, violation_category_id, coordinates,
                    latitude, longitude, json_folder_id, json_file_path, json_full_name,
                    photo_file_path, photo_folder_id, photo_full_name
                )
            )

    def get_id(self, table, entry) -> int:

        if not entry:
            print(f"no entry {entry = }")
            return 0

        query = f"SELECT `id` FROM `{table}` WHERE `title` = ?"

        with self.connection:
            result = self.cursor.execute(query, (entry,)).fetchall()
            if not result:
                print(f"no matches found {entry = } in {table}")
                sys.exit()

            entry_id = 0
            for row in result:
                entry_id = int(row[0])
                return entry_id

            if entry_id == 0:
                print(f"no matches found {entry = } in {table}")
                sys.exit()

    # def get_location_id(self, location: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_location` WHERE `title` = ?",
    #                                      (location,)).fetchall()
    #         if not result:
    #             print(f"no matches found {location = } in core_location")
    #             sys.exit()
    #
    #         location_id = 0
    #         for row in result:
    #             location_id = int(row[0])
    #             return location_id
    #
    #         if location_id == 0:
    #             print(f"no matches found {location_id = } in core_location")
    #             sys.exit()
    #
    # def get_work_shift_id(self, work_shift: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_workshift` WHERE `title` = ?",
    #                                      (work_shift,)).fetchall()
    #         if not result:
    #             print(f"no matches found {work_shift = } in core_workshift")
    #             sys.exit()
    #
    #         work_shift_id = 0
    #         for row in result:
    #             work_shift_id = int(row[0])
    #             return work_shift_id
    #
    #         if work_shift_id == 0:
    #             print(f"no matches found {work_shift = } in core_workshift")
    #             sys.exit()
    #
    # def get_main_category_id(self, main_category: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_maincategory` WHERE `title` = ?",
    #                                      (main_category,)).fetchall()
    #         if not result:
    #             print(f"no matches found {main_category = } in core_maincategory")
    #             sys.exit()
    #
    #         main_category_id = 0
    #         for row in result:
    #             main_category_id = int(row[0])
    #             return main_category_id
    #
    #         if main_category_id == 0:
    #             print(f"no matches found {main_category = } in core_maincategory")
    #             sys.exit()
    #
    # def get_general_contractor_id(self, general_contractor: str) -> int:
    #     """Поиск имени изера """
    #
    #     general_contractor = general_contractor.replace("'", "")
    #     # general_contractor = general_contractor.replace("МИП-Строй№1(?)", "МИП - Строй 1(?)")
    #
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_generalcontractor` WHERE `title` = ?",
    #                                      (general_contractor,)).fetchall()
    #         if not result:
    #             print(f"no matches found {general_contractor = } in core_generalcontractor")
    #             sys.exit()
    #
    #         general_contractor_id = 0
    #         for row in result:
    #             general_contractor_id = int(row[0])
    #             return general_contractor_id
    #
    #         if general_contractor_id == 0:
    #             print(f"no matches found {general_contractor = } in core_generalcontractor")
    #             sys.exit()
    #
    # def get_category_id(self, category: str) -> int:
    #     """Поиск имени изера """
    #
    #     category = category.replace("Пожарная безопасность", "Пожарная безопасность_")
    #     category = category.replace("Промышленная безопасность", "Промышленная безопасность_")
    #     category = category.replace("Промышленная безопасность__", "Промышленная безопасность_")
    #
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_category` WHERE `title` = ?",
    #                                      (category,)).fetchall()
    #         if not result:
    #             print(f"no matches found {category = } in core_category")
    #             sys.exit()
    #
    #         category_id = 0
    #         for row in result:
    #             category_id = int(row[0])
    #             return category_id
    #
    #         if category_id == 0:
    #             print(f"no matches found {category = } in core_category")
    #             sys.exit()
    #
    # def get_elimination_time_id(self, elimination_time: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_eliminationtime` WHERE `title` = ?",
    #                                      (elimination_time,)).fetchall()
    #         if not result:
    #             print(f"no matches found {elimination_time = } in core_eliminationtime")
    #             sys.exit()
    #
    #         elimination_time_id = 0
    #         for row in result:
    #             elimination_time_id = int(row[0])
    #             return elimination_time_id
    #
    #         if elimination_time_id == 0:
    #             print(f"no matches found {elimination_time = } in core_eliminationtime")
    #             sys.exit()
    #
    # def get_incident_level_id(self, incident_level: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_incidentlevel` WHERE `title` = ?",
    #                                      (incident_level,)).fetchall()
    #         if not result:
    #             print(f"no matches found {incident_level = } in core_incidentlevel")
    #             sys.exit()
    #
    #         incident_level_id = 0
    #         for row in result:
    #             incident_level_id = int(row[0])
    #             return incident_level_id
    #
    #         if incident_level_id == 0:
    #             print(f"no matches found {incident_level = } in core_incidentlevel")
    #             sys.exit()
    #
    # def get_violation_category_id(self, violation_category: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_violationcategory` WHERE `title` = ?",
    #                                      (violation_category,)).fetchall()
    #         if not result:
    #             print(f"no matches found {violation_category = } in core_violationcategory")
    #             sys.exit()
    #
    #         violation_category_id = 0
    #         for row in result:
    #             violation_category_id = int(row[0])
    #             return violation_category_id
    #
    #         if violation_category_id == 0:
    #             print(f"no matches found {violation_category = } in core_violationcategory")
    #             sys.exit()
    #
    # def get_act_required_id(self, act_required: str) -> int:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `id` FROM `core_actrequired` WHERE `title` = ?",
    #                                      (act_required,)).fetchall()
    #         if not result:
    #             print(f"no matches found {act_required = } in core_actrequired")
    #             sys.exit()
    #
    #         act_required_id = 0
    #         for row in result:
    #             act_required_id = int(row[0])
    #             return act_required_id
    #
    #         if act_required_id == 0:
    #             print(f"no matches found {act_required = } in core_actrequired")
    #             sys.exit()

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


violation_file: str = 'C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\373084462' \
                      '\\data_file\\20.07.2022\\json\\report_data___20.07.2022___373084462___22027.json'


async def run_init():
    violation = await read_json_file(file=violation_file)

    if not violation:
        print('ERROR')
        exit(1)

    DataBase().add_violation(violation=violation)


# async def write_json(violation):
#     """Запись в файл"""
#     if not os.path.isfile(violation['json_full_name']):
#         print(f"FileNotFoundError {violation['json_full_name']} ")
#
#         date_violation = violation['file_id'].split('___')[0]
#
#         violation['json_full_name'] = \
#             f"C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot\\user_data\\373084462\\data_file" \
#             f"\\{date_violation}\\json\\report_data___{violation['file_id']}.json"
#         violation['photo_full_name'] = \
#             f"C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot\\user_data\\373084462\\data_file" \
#             f"\\{date_violation}\\photo\\report_data___{violation['file_id']}.jpg"
#
#         await write_json_file(data=violation, name=violation['json_full_name'])
#         return
#
#     await write_json_file(data=violation, name=violation['json_full_name'])


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

        # if not violation.get("work_shift"):
        #     violation["work_shift"] = user_data_json_file.get("work_shift")
        #     await write_json(violation=violation)
        #
        # if not violation.get("function"):
        #     violation["function"] = user_data_json_file.get("function")
        #     await write_json(violation=violation)
        #
        # if not violation.get("name"):
        #     violation["name"] = user_data_json_file.get("name")
        #     await write_json(violation=violation)
        #
        # if not violation.get("parent_id"):
        #     violation["parent_id"] = user_data_json_file.get("parent_id")
        #     await write_json(violation=violation)
        #
        #
        # if not violation.get('general_contractor'):
        #     print(f"ERROR file: {file_id} don't get 'general_contractor' parameter")
        #     error_counter += 1
        #     general_contractor_counter += 1
        #
        #     os.remove(violation_file)
        #     print(f"file: {violation_file} is remove")
        #     continue
        #
        # if not violation.get('elimination_time'):
        #     print(f"ERROR file: {file_id} don't get 'elimination_time' parameter")
        #     error_counter += 1
        #     elimination_time_counter += 1
        #     violation['elimination_time'] = '1 день'
        #     await write_json(violation=violation)
        #     continue
        #
        # if not violation.get('incident_level'):
        #     print(f"ERROR file: {file_id} don't get 'incident_level' parameter")
        #     error_counter += 1
        #     incident_level_counter += 1
        #     violation['incident_level'] = 'Без последствий'
        #     await write_json(violation=violation)
        #     continue
        #
        # if not violation.get('act_required'):
        #     print(f"ERROR file: {file_id} don't get 'act_required' parameter")
        #     error_counter += 1
        #     act_required_counter += 1
        #     os.remove(violation_file)
        #     print(f"file: {violation_file} is remove")
        #     continue
        #
        # if not violation.get('comment'):
        #     print(f"ERROR file: {file_id} don't get 'comment' parameter")
        #     error_counter += 1
        #     comment_counter += 1
        #     continue

        if not DataBase().violation_exists(file_id):
            location_id = await get_entry(violation=violation, query="location",
                                          user_data_json_file=user_data_json_file)
            print(f'{location_id = }')

            # main_category_id = DataBase().get_id(entry=violation.get("main_category", None))
            main_category_id = await get_entry(violation=violation, query="main_category",
                                               user_data_json_file=user_data_json_file)

            print(f'{main_category_id = }')

            DataBase().add_violation(violation=violation)
            print(f"{counter} file {violation.get('file_id')} add in db {DataBase().db_file}")

    print(f"errors {error_counter} in {len(json_file_list)} items")
    print(f"general_contractor_counter {general_contractor_counter} in {error_counter} items")
    print(f"elimination_time_counter {elimination_time_counter} in {error_counter} items")
    print(f"act_required_counter {act_required_counter} in {error_counter} items")
    print(f"incident_level_counter {incident_level_counter} in {error_counter} items")
    print(f"comment_counter {comment_counter} in {error_counter} items")


if __name__ == '__main__':
    # db_file: str = WORK_PATH + '\\HSEViolationsDataBase.db'  # type: ignore

    # asyncio.run(run_init())

    user_chat_id = '373084462'
    params: dict = {
        'all_files': True,
        'file_path': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{user_chat_id}/data_file/20.07.2022/",
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
