import asyncio
import sqlite3
import traceback
from datetime import datetime, timedelta

from apps.core.bot.messages.messages import LogMessage
from apps.core.settyngs import get_sett
from config.config import DATA_BASE_DIR
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


class DataBaseForCheck:
    """Основной класс работы с базой данных для класса PeriodicCheck
    """

    def __init__(self):
        self.db_file: str = DATA_BASE_DIR
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    async def get_data_list(self, query: str = None) -> list:
        """Получение данных из таблицы по запросу 'query'"""
        if not query:
            return []
        try:
            with self.connection:
                return self.cursor.execute(query).fetchall()
        except sqlite3.OperationalError as err:
            logger.error(f"error {repr(err)}")
            return []

    async def get_table_headers(self, table_name: str = None) -> list[str]:
        """Получение всех заголовков таблицы core_violations

        :param table_name: имя таблицы в которой осуществляется поиск
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

    async def get_dict_data_from_table_from_id(self, table_name: str, id: int) -> dict:
        """Получение данных dict из таблицы table_name по id
        :param table_name: имя таблицы в которой осуществляется поиск
        :param id: id записи
        :return dict('header': item_value, ...)
        """

        query_kwargs: dict = {
            "action": 'SELECT',
            "subject": '*',
            "conditions": {
                "id": id,
            },
        }
        query: str = await QueryConstructor(None, table_name, **query_kwargs).prepare_data()

        val: list = await self.get_data_list(query=query)
        values: list = val[0] if val else []
        headers: list = [item[1] for item in await self.get_table_headers(table_name)]

        return dict((header, item_value) for header, item_value in zip(headers, values))

    async def update_column_value(self, column_name: str, value: str, violation_id: str):
        """Обновление записи id в database

        :param violation_id: id записи
        :param value:  значение для записи в столбец
        :param column_name: столбец
        """
        # TODO заменить на вызов конструктора QueryConstructor
        query: str = f"UPDATE `core_violations` SET {column_name} = ? WHERE `id` = ?"

        logger.debug(f'{column_name = } {value = }')
        with self.connection:
            self.cursor.execute(query, (value, violation_id,))
        self.connection.commit()


async def periodic_check_data_base() -> None:
    """Периодическая проверка базы данных.
    Проверяет дату final_date_elimination в DataBase

    """
    while True:
        work_period_hour: int = get_sett(cat='param', param='check_work_period_hour').get_set()

        if not get_sett(cat='check', param='check_data_base').get_set():
            logger.warning(f'{await fanc_name()} not access')
            await asyncio.sleep(work_period_hour)
            continue

        await check_violations_final_date_elimination()
        await check_violations_status()

        logger.info(f"{LogMessage.Check.complete_successfully} ::: {await get_now()}")

        await asyncio.sleep(work_period_hour)


async def check_violations_final_date_elimination() -> bool:
    """Проверка записей в core_violations с истекшей датой устранения

    :return:
    """
    query_kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "finished_id": "0",
            "status_id": "== 2"
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    list_violations: list = await get_list_violations_for_query(query=query)

    if not list_violations:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")

    counter: int = 0
    for violation in list_violations:

        created_at, final_date = await get_dates_violation(violation)
        if created_at is None or final_date is None:
            continue

        if datetime.now() >= final_date:
            violation_id = violation.get('id', None)
            logger.info(f'{violation_id = }  now >= final_date_elimination')
            await DataBaseForCheck().update_column_value(column_name='finished_id',
                                                         value=str(2),
                                                         violation_id=str(violation_id)
                                                         )
            counter += 1

    if not counter:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")

    return True


async def check_violations_status():
    """Проверка поля status

    :return:
    """
    query_kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "finished_id": "1",
            "status_id": "!= 1"
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    list_violations: list = await get_list_violations_for_query(query=query)

    if not list_violations:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")
        return []

    counter: int = 0
    for violation in list_violations:
        violation_id = violation.get('id', None)
        status_id = violation.get('status_id', None)
        finished_id = violation.get('finished_id', None)

        if finished_id == 1 and status_id != 1:
            logger.info(f'{violation_id= } ::: {finished_id = } ::: {status_id = }')
            await DataBaseForCheck().update_column_value(
                column_name='status_id',
                value=str(1),
                violation_id=str(violation_id)
            )
            counter += 1

    if not counter:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")


async def get_list_violations_for_query(query: str) -> list:
    """Возвращает list с нарушениями

    :return: list
    """

    if not query:
        logger.error(f"{LogMessage.Check.no_query} ::: {await get_now()}")
        return []

    list_violations: list = []
    table_name = 'core_violations'

    violations_data: list = await DataBaseForCheck().get_data_list(query=query)

    if not violations_data:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")
        return []

    headers = await DataBaseForCheck().get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    for violation in violations_data:
        item_dict: dict = dict((header, item_value) for header, item_value in zip(clean_headers, violation))
        list_violations.append(item_dict)

    return list_violations


async def get_dates_violation(violation: dict):
    """Возвращает дату регистрации и конечную даты акта

    """
    created_at = violation.get('created_at', None)

    if created_at is None:
        logger.debug(f"{LogMessage.Check.date_created_at} ::: {await get_now()}")
        return None, None

    elimination_days: int = await get_elimination_days(e_time=violation.get('elimination_time_id', None))

    if not elimination_days:
        elimination_days = 0

    date_now: datetime = datetime.strptime(created_at, '%Y-%m-%d')
    final_date_elimination = date_now + timedelta(days=elimination_days)

    return created_at, final_date_elimination


async def get_elimination_days(e_time: int) -> int:
    """Получение количества дней на устранение

    :return:
    """
    if e_time is None:
        return 0

    elimination_time: dict = await DataBaseForCheck().get_dict_data_from_table_from_id(
        table_name='core_eliminationtime',
        id=e_time
    )
    elimination_days = elimination_time.get('days', None)
    return elimination_days


async def get_now() -> str:
    """Возвращает текущую дату и время.
    :return: str
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


async def test():
    await periodic_check_data_base()


if __name__ == '__main__':
    asyncio.run(test())
