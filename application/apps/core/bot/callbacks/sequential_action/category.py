from __future__ import annotations
from loader import logger

logger.debug(f"{__name__} start import")
import traceback
import asyncio
import inspect
import os.path
from apps.core.database.query_constructor import QueryConstructor
from apps.core.database.db_utils import (db_get_data_list_no_async,
                                         db_get_id,
                                         db_get_table_headers_no_async)

logger.debug(f"{__name__} finish import")

filename = inspect.getframeinfo(inspect.currentframe()).filename
PATH = os.path.dirname(os.path.abspath(filename))

REGISTRATION_DATA_LIST: list = [
    "ФИО",
    "Должность",
    "Место работы",
    "Смена",
    "Телефон"
]

HEADLINES_DATA_LIST: list = [
    "Руководитель строительства",
    "Инженер СК",
    "Подрядчик",
    "Субподрядчик",
    "Вид обхода",
    "Представитель подрядчика",
    "Представитель субподрядчика"
]

VIOLATIONS_DATA_LIST: list = [
    "Описание нарушения",
    "Комментарий к нарушению",
    "Основное направление",
    "Количество дней на устранение",
    "Степень опасности ситуации",
    "Требуется ли оформление акта?",
    "Подрядная организация",
    "Категория нарушения",
    "Уровень происшествия"
]

ADMIN_MENU_LIST: list = [
    'Показать всех пользователей',
    'Оповещение'
]

_PREFIX_ND: str = 'nrm_doc_'
_PREFIX_POZ: str = 'nrm_poz_'


def convert_category_name(category_in_db: str) -> str:
    """

    :param category_in_db:
    :return:
    """
    all_category_in_db: dict = {
        'MAIN_CATEGORY': 'core_maincategory',
        'CATEGORY': 'core_category',
        'VIOLATION_CATEGORY': 'core_violationcategory',
        'GENERAL_CONTRACTORS': 'core_generalcontractor',
        'ACT_REQUIRED': 'core_actrequired',
        'INCIDENT_LEVEL': 'core_incidentlevel',
        'ELIMINATION_TIME': 'core_eliminationtime',
        'LOCATIONS': 'core_location',
        'NORMATIVE_DOCUMENTS': 'core_normativedocuments',
        'MAIN_LOCATIONS': 'core_mainlocation',
        'SUB_LOCATIONS': 'core_sublocation',

    }
    return all_category_in_db.get(category_in_db, None)


def add_null_value_to_ziped_list(zip_list: list) -> list:
    """Добавление значения заглушки
    
    :param zip_list: 
    :return: 
    """

    zip_list.append(
        {
            'title': 'Нет нужной записи'
        }
    )

    return zip_list


def add_null_value_to_list(zip_list: list, condition: str, db_table_name: str) -> list:
    """

    :param db_table_name: имя базы данных
    :param condition:
    :param zip_list:
    :return:
    """

    if condition == 'data_list':
        zip_list.append('Нет нужной записи')

    if condition == 'short_title':
        if db_table_name == 'core_normativedocuments':
            zip_list.append(_PREFIX_ND + '0')

        if db_table_name == 'core_sublocation':
            zip_list.append(_PREFIX_POZ + '0')

    return zip_list


def add_hashtags(datas_from_bd, db_table_name: str, item_id) -> list:
    """Добавление хештегов

    :param db_table_name: имя базы данных
    :param datas_from_bd:
    :param item_id:
    :return:
    """

    hashtags: list = get_hashtags(db_table_name, item_id=item_id)
    logger.debug(f'{__name__} {fanc_name()} {hashtags = }')

    if not hashtags:
        return datas_from_bd

    for tag in hashtags:
        datas_from_bd.insert(0, tag)

    return datas_from_bd


def get_category_data_list_whits_single_condition(db_table_name: str, item_id: int, single_condition: str) -> list:
    """ Получение данных если single_condition

    :param single_condition:
    :param item_id:
    :param db_table_name: имя базы данных
    :return: list
    """
    clean_datas_query: list = []
    query: str = ""

    # TODO заменить на вызов конструктора QueryConstructor
    if db_table_name == 'core_sublocation':
        query: str = f'SELECT * FROM {db_table_name} WHERE `main_location_id` == {item_id}'
        logger.debug(f'{__name__} {fanc_name()} {query = }')

    # TODO заменить на вызов конструктора QueryConstructor
    if db_table_name == 'core_normativedocuments':
        query: str = f'SELECT * FROM {db_table_name} WHERE `category_id` == {item_id}'
        logger.debug(f'{__name__} {fanc_name()} {query = }')

    datas_query: list = db_get_data_list_no_async(query=query)

    if not datas_query:
        return []
    if not isinstance(datas_query, list):
        return []

    if single_condition == 'short_title':

        if db_table_name == 'core_sublocation':
            clean_datas_query: list = [_PREFIX_POZ + str(item[0]) for item in datas_query]

        if db_table_name == 'core_normativedocuments':
            clean_datas_query: list = [_PREFIX_ND + str(item[0]) for item in datas_query]

        return clean_datas_query

    if single_condition == 'data_list':
        clean_datas_query: list = [item[2] for item in datas_query]
        return clean_datas_query


def get_category_data_list_whits_dict_condition(db_table_name, dict_condition) -> list:
    """ Получение данных если single_condition

    :return:
    """

    if not isinstance(dict_condition, dict):
        return []

    if not dict_condition.get("data", None):
        return []

    if db_table_name == 'core_sublocation':
        item_id = dict_condition.get("data", None).replace(_PREFIX_POZ, '')

    if db_table_name == 'core_normativedocuments':
        item_id = dict_condition.get("data", None).replace(_PREFIX_ND, '')

    # TODO заменить на вызов конструктора QueryConstructor
    query: str = f'SELECT * FROM {db_table_name} WHERE `id` == {item_id}'
    logger.debug(f'{__name__} {fanc_name()} {query = }')
    datas_query: list = db_get_data_list_no_async(query=query)

    if not datas_query:
        return []
    if not isinstance(datas_query, list):
        return []

    table_headers: list = db_get_table_headers_no_async(db_table_name=db_table_name)
    headers = [item[1] for item in table_headers]
    item_datas = list(datas_query[0])

    data_dict: dict = {}
    for header, item_data in zip(headers, item_datas):
        data_dict[header] = item_data

    condition = dict_condition.get("condition", None)
    if not condition:
        return [data_dict]


def get_category_data_list_whits_condition(db_table_name: str, category, condition: str | dict) -> list:
    """Получение

    :param category:
    :param db_table_name: имя базы данных
    :type condition: Union[str, dict]

    """
    main_table_name: str = 'core_violations'

    if db_table_name == 'core_normativedocuments':
        main_table_name = 'core_category'

    if db_table_name == 'core_sublocation':
        main_table_name = 'core_mainlocation'

    category_id = asyncio.run(db_get_id(table=main_table_name, entry=category, calling_function_name=fanc_name()))

    if category_id is None:
        return []

    if isinstance(condition, str):
        datas_from_bd: list = get_category_data_list_whits_single_condition(
            db_table_name=db_table_name,
            item_id=category_id,
            single_condition=condition
        )

        datas_from_bd: list = add_hashtags(datas_from_bd, db_table_name=db_table_name, item_id=category_id)

        datas_from_bd: list = add_null_value_to_list(
            datas_from_bd, condition, db_table_name
        )
        return datas_from_bd

    if isinstance(condition, dict):
        datas_from_bd: list = get_category_data_list_whits_dict_condition(
            db_table_name=db_table_name,
            dict_condition=condition
        )
        datas_from_bd: list = add_hashtags(datas_from_bd, db_table_name=db_table_name, item_id=category_id)
        datas_from_bd: list = add_null_value_to_ziped_list(datas_from_bd)
        return datas_from_bd
    return []


def get_data_from_db(db_table_name: str) -> list:
    """Получение
    """

    # TODO заменить на вызов конструктора QueryConstructor
    query: str = f'SELECT * FROM {db_table_name}'
    datas_query: list = db_get_data_list_no_async(query=query)
    headers: list = [item[1] for item in db_get_table_headers_no_async(db_table_name=db_table_name)]

    if not isinstance(datas_query, list):
        return []

    if 'short_title' in headers:
        data_list = [data[2] for data in datas_query]
        return data_list

    if datas_query:
        logger.debug(f'retrieved data from database: {datas_query}')
        data_list = [data[1] for data in datas_query]
        return data_list

    return []


def get_data_list(category_in_db: str = None, category: str = None, condition: str | dict = None) -> list:
    """ Функция получения данных из базы данных. При отсутствии данных поиск в json.
    При наличии condition - формирование данных согласно  condition

    :param category:
    :param category_in_db:
    :param condition:
    :return: data_list or [ ]
    """

    db_table_name = convert_category_name(category_in_db)

    if not db_table_name:
        return []

    if category and condition:
        clean_datas_query: list = get_category_data_list_whits_condition(
            db_table_name=db_table_name,
            category=category,
            condition=condition
        )
        logger.debug(f'get_category_data_list from db with condition: {clean_datas_query}')
        return clean_datas_query

    data_list: list = get_data_from_db(db_table_name=db_table_name)

    if not data_list:
        return []

    logger.debug(f'{data_list = }')
    return data_list


def get_data_with_hashtags(db_table_name: str, item_id: int) -> list:
    """Получение хештегов

    :param db_table_name: имя базы данных
    :param item_id:
    :return: hashtags: [#str, ...]
    """

    if not item_id:
        logger.debug(f'{db_table_name = } {item_id = }')
        return []

    hashtags: list = get_hashtags(db_table_name, item_id=item_id)
    logger.debug(f'{hashtags = }')

    return hashtags


def get_hashtags(db_table_name: str, item_id: int = None) -> list:
    """Возвращает список хештегов для найденных данных"""

    if not db_table_name:
        return []

    table_headers: list = db_get_table_headers_no_async(db_table_name=db_table_name)
    clean_headers = [item[1] for item in table_headers]

    if 'hashtags' not in clean_headers:
        return []

    if db_table_name == 'core_normativedocuments':
        kwargs = {
            "action": 'SELECT', "subject": 'hashtags',
            "conditions": {
                "category_id": item_id,
            }
        }
    elif db_table_name == 'core_sublocation':
        kwargs = {
            "action": 'SELECT', "subject": 'hashtags',
            "conditions": {
                "main_location_id": item_id
            }
        }
    else:
        return []

    query = asyncio.run(QueryConstructor(None, db_table_name, **kwargs).prepare_data())
    data_list: list = db_get_data_list_no_async(query=query)

    if not data_list:
        logger.error(f'{__name__} {fanc_name()} {query = } {db_table_name = } {data_list = }')
        return []

    list_of_lists = [item[0].split(';') for item in data_list if isinstance(item[0], str)]
    if not list_of_lists: return []

    data_unpac = [item for sublist in list_of_lists for item in sublist]
    if not data_unpac: return []

    clean_data_unpac = [item.lstrip().rstrip() for item in data_unpac]

    logger.debug(f'{len(clean_data_unpac) = }')

    unique_hash_t = list(set(clean_data_unpac))
    if not unique_hash_t: return []

    return unique_hash_t


async def test():
    # data_list = get_data_list("MAIN_LOCATIONS", condition='short_title')
    # logger.info(f'{__name__} {fanc_name()} {data_list = }')
    #
    # for i in data_list:
    #     short_title = get_data_list('sub_locations'.upper(),
    #                                 category=i,
    #                                 condition='short_title'
    #                                 )
    #     logger.info(f'{__name__} {fanc_name()} {short_title =}')

    db_table_name = 'core_normativedocuments'
    condition = 'short_title'
    category_id = 5

    datas_from_bd: list = get_category_data_list_whits_single_condition(
        db_table_name=db_table_name,
        item_id=category_id,
        single_condition=condition
    )

    logger.info(f'{__name__} {fanc_name()} {datas_from_bd = }')

    datas_from_bd: list = add_hashtags(datas_from_bd, db_table_name=db_table_name, item_id=category_id)

    logger.info(f'{__name__} {fanc_name()} {datas_from_bd = }')

    datas_from_bd: list = add_null_value_to_list(
        datas_from_bd, condition=condition, db_table_name=db_table_name
    )

    logger.info(f'{__name__} {fanc_name()} {datas_from_bd = }')


def fanc_name() -> str:
    """Возвращает имя вызываемой функции"""
    stack = traceback.extract_stack()
    return str(stack[-2][2])


if __name__ == "__main__":
    asyncio.run(test())
