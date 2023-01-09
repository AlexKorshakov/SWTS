from pandas import DataFrame

from apps.core.database.DataBase import DataBase


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
