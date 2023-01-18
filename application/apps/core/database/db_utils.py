import asyncio
from datetime import datetime

from pandas import DataFrame

from apps.core.database.DataBase import DataBase
from apps.core.utils.secondary_functions.get_part_date import get_year_message


async def db_check_record_existence(file_id: int) -> bool:
    """Проверка наличия записи в БД

    :type file_id: int - id записи
    :return: bool is_exists
    """
    is_exists: bool = DataBase().violation_exists(file_id=file_id)
    if is_exists:
        return True

    return False


async def db_add_violation(violation_data: dict) -> bool:
    """Добавление записи в БД

    :param violation_data: dict -  dict с данными для записи в БД
    :return: bool violation_exists
    """
    is_added: bool = DataBase().add_violation(violation=violation_data)
    if is_added:
        return True

    return False


async def db_get_data_dict_from_table_with_id(table_name: str, post_id: int, query: str = None) -> dict:
    """Получение данных из table_name с помощью post_id

    :return: dict - dict с данными
    """

    data_exists: dict = DataBase().get_dict_data_from_table_from_id(
        table_name=table_name,
        id=post_id,
        query=query
    )

    return data_exists


async def db_get_categories() -> list:
    query: str = "SELECT `title` FROM `core_category`"
    categories: list = await db_get_data_list(query=query)
    clean_categories: list = [item[0] for item in categories]

    return clean_categories


async def db_del_violations(violation: dict) -> list:
    """Удаление данных violation из Database

    :param violation dict данные записи для удаления
    :return: list
    """

    file_id = violation['file_id']
    result = DataBase().delete_single_violation(file_id=file_id)
    return result


async def db_get_data_list(query: str) -> list:
    """Получение list с данными по запросу query

    :return: list
    """
    datas_query: list = DataBase().get_data_list(query=query)
    return datas_query


async def db_get_single_violation(file_id: str) -> list:
    """Получение данных нарушения по file_id из core_violations

    :return: list
    """

    violation_list: list = DataBase().get_single_violation(file_id=file_id)
    return violation_list


async def db_get_table_headers(table_name: str = None) -> list:
    """Получение заголовков таблицы

    :return:
    """

    table_headers: list = DataBase().get_table_headers(table_name)
    return table_headers


async def db_get_id_violation(file_id) -> int:
    """Получение id записи

    :return: int
    """

    vi_id: int = DataBase().get_id_violation(file_id=file_id)
    return vi_id


async def db_get_id(table, entry, file_id, name) -> int:
    """Получение id записи по значению title из соответствующий таблицы table

    :return: int
    """
    value: int = DataBase().get_id(
        table=table,
        entry=entry,
        file_id=file_id,
        name=name
    )
    return value


async def db_update_column_value(column_name, value, violation_id) -> bool:
    """

    :return:
    """

    result: bool = DataBase().update_column_value(
        column_name=column_name,
        value=value,
        id=str(violation_id)
    )
    return result


async def db_get_full_title(table_name: str, short_title: str) -> list:
    """

    :return:
    """
    full_title = DataBase().get_full_title(table_name=table_name, short_title=short_title)
    return full_title


async def db_get_max_max_number() -> int:
    """Получение номера акта из Database `core_reestreacts`

    :return: int act_num: номер акта - предписания
    """
    act_num: int = DataBase().get_max_max_number()
    return act_num


async def db_set_act_value(act_data_dict: DataFrame, act_number: int, act_date: str) -> bool:
    """

    :return:
    """
    act_is_created: bool = DataBase().set_act_value(act_data_dict=act_data_dict,
                                                    act_number=act_number,
                                                    act_date=act_date)
    return act_is_created


async def db_get_username(user_id: int) -> str:
    """Получение username из core_hseuser по user_id

    :return:
    """
    if not user_id:
        print(f'ERROR: No user_id foe db_get_username ')

    query: str = f'SELECT * FROM `core_hseuser` WHERE `hse_telegram_id` = {user_id}'
    datas_query: list = DataBase().get_data_list(query=query)
    username = datas_query[0][4]

    return username


async def db_get_dict_userdata(user_id: int) -> dict:
    """Получение userdata из core_hseuser по user_id

    :return: dict
    """
    if not user_id:
        print(f'ERROR: No user_id foe db_get_username ')
        return {}
    table_name: str = 'core_hseuser'

    headers: list = await db_get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    query: str = f'SELECT * FROM {table_name} WHERE `hse_telegram_id` = {user_id}'
    datas_query: list = DataBase().get_data_list(query=query)
    clean_values: list = datas_query[0]

    return dict((header, item_value) for header, item_value in zip(clean_headers, clean_values))


async def db_get_period_for_current_week(current_week: str, current_year: str = None) -> list:
    """Получение данных из core_week по week_number

    :return:
    """
    if not current_week:
        print(f'ERROR: No user_id foe db_get_username ')

    if not current_year:
        current_year = await get_year_message(current_date=datetime.now())

    query: str = f'SELECT * FROM `core_week` WHERE `week_number` = {current_week}'
    datas_query: list = DataBase().get_data_list(query=query)
    period_data = datas_query[0]

    table_headers: list = DataBase().get_table_headers('core_week')
    headers = [row[1] for row in table_headers]
    period_dict = dict(zip(headers, period_data))

    period = [
        period_dict.get(f'start_{current_year}', None),
        period_dict.get(f'end_{current_year}', None)
    ]

    return period


def db_get_data_list_no_async(query: str) -> list:
    """Получение list с данными по запросу query

    :return: list
    """
    datas_query: list = DataBase().get_data_list(query=query)
    return datas_query


def db_get_table_headers_no_async(db_table_name: str) -> list:
    """

    :return:
    """

    result_list: list = DataBase().get_table_headers(table_name=db_table_name)
    return result_list


def db_get_id_no_async(table, entry, file_id: str = None, name=None) -> int:
    """Получение id записи по значению title из соответствующий таблицы table

    :return: int
    """
    value: int = DataBase().get_id(
        table=table,
        entry=entry,
        file_id=file_id,
        name=name
    )
    return value
