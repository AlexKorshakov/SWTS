import asyncio
import sqlite3
from datetime import datetime, timedelta

from config.config import DATA_BASE_DIR
from loader import logger

PERIOD = 60*30


class DataBase:

    def __init__(self):
        self.db_file: str = DATA_BASE_DIR
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def get_data_list(self, query: str = None) -> list:
        """Получение данных из таблицы по запросу 'query'"""
        if not query:
            return []
        try:
            with self.connection:
                return self.cursor.execute(query).fetchall()
        except sqlite3.OperationalError as err:
            logger.error(f"error {repr(err)}")

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

    def get_dict_data_from_table_from_id(self, table_name: str, violation_id: int) -> dict:

        query: str = f'SELECT * ' \
                     f'FROM {table_name} ' \
                     f'WHERE `id` = {violation_id} '

        headers: list = [item[1] for item in self.get_table_headers(table_name)]
        values: list = self.get_data_list(query=query)[0]

        return dict((header, item_value) for header, item_value in zip(headers, values))

    def update_column_value(self, column_name: str, value: str, violation_id: str):
        """Обновление записи id в database

        :param violation_id: id записи
        :param value:  значение для записи в столбец
        :param column_name: столбец
        """

        query: str = f"UPDATE `core_violations` SET {column_name} = ? WHERE `id` = ?"
        logger.debug(f'{column_name = } {value = }')
        with self.connection:
            self.cursor.execute(query, (value, violation_id,))
        self.connection.commit()


async def get_clean_headers(table_name: str) -> list:
    """Получение заголовков таблицы

    :param
    """

    if not table_name:
        return []

    headers = DataBase().get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]
    logger.debug(clean_headers)
    return clean_headers


async def periodic_check_data_base():
    """Периодическая проверка базы данных

    :return:
    """
    print(f'run periodic_check_data_base')
    while True:
        await check_violations_final_date_elimination()
        await check_violations_status()

        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logger.info(f"check DataBase complete successfully ::: {now}")
        # print(f"check DataBase complete successfully ::: {now}")

        await asyncio.sleep(PERIOD)


async def check_violations_final_date_elimination():
    """Проверка записей в core_violations с истекшей датой устранения

    :return:
    """
    table_name = 'core_violations'
    query: str = f'SELECT * FROM {table_name} WHERE `finished_id` == 0 ' \
                 f'AND `status_id` == 2'
    violations_data: list = DataBase().get_data_list(query=query)

    if not violations_data:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logger.debug(f"check_violations_final_date_elimination ::: No violations for check in DataBase ::: {now}")
        # print(f"check_violations_final_date_elimination ::: No violations for check in DataBase ::: {now}")
        return

    headers = DataBase().get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    list_violations: list = []
    for violation in violations_data:
        item_dict: dict = dict((header, item_value) for header, item_value in zip(clean_headers, violation))
        list_violations.append(item_dict)

    counter: int = 0
    for violation in list_violations:

        violation_id = violation.get('id', None)
        e_time = violation.get('elimination_time_id', None)

        elimination_time: dict = DataBase().get_dict_data_from_table_from_id(
            table_name='core_eliminationtime',
            violation_id=e_time
        )
        elimination_days = elimination_time.get('days', None)
        created_at = violation.get('created_at', None)

        if not created_at:
            continue

        registered_date: datetime = datetime.strptime(created_at, '%Y-%m-%d')
        final_date_elimination = registered_date + timedelta(days=elimination_days)

        if datetime.now() >= final_date_elimination:
            logger.info(f'{violation_id= }  now >= final_date_elimination')
            DataBase().update_column_value(column_name='finished_id',
                                           value=str(2),
                                           violation_id=str(violation_id)
                                           )
            counter += 1

    if not counter:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logger.debug(f"check_violations_final_date_elimination ::: No violations for check in DataBase ::: {now}")
        # print(f"check_violations_final_date_elimination ::: No violations for check in DataBase ::: {now}")


async def check_violations_status():
    """

    :return:
    """

    table_name = 'core_violations'
    query: str = f'SELECT * FROM {table_name} WHERE `finished_id` == 1 ' \
                 f'AND `status_id` != 1'
    violations_data: list = DataBase().get_data_list(query=query)

    if not violations_data:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logger.debug(f"check_violations_status ::: No violations for check in DataBase ::: {now}")
        # print(f"check_violations_status ::: No violations for check in DataBase ::: {now}")
        return

    headers = DataBase().get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    list_violations: list = []
    for violation in violations_data:
        item_dict: dict = dict((header, item_value) for header, item_value in zip(clean_headers, violation))
        list_violations.append(item_dict)

    counter: int = 0
    for violation in list_violations:
        violation_id = violation.get('id', None)
        status_id = violation.get('status_id', None)
        finished_id = violation.get('finished_id', None)

        if finished_id == 1 and status_id != 1:
            logger.info(f'{violation_id= } ::: {finished_id = } ::: {status_id = }')
            DataBase().update_column_value(column_name='status_id',
                                           value=str(1),
                                           violation_id=str(violation_id)
                                           )
            counter += 1

    if not counter:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logger.debug(f"check_violations_status ::: No violations for check in DataBase ::: {now}")
        # print(f"check_violations_status ::: No violations for check in DataBase ::: {now}")


async def periodic_check_work():
    """Периодическое напоминание о работе"""
    print(f'run periodic_check_work')
    while True:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logger.info(f"i'm work ::: {now}")
        print(f"i'm work ::: {now}")
        await asyncio.sleep(PERIOD)


if __name__ == '__main__':
    asyncio.run(periodic_check_data_base())
