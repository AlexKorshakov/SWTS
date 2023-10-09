from __future__ import annotations
import asyncio
import traceback


from apps.MyBot import MyBot
from apps.core.database.db_utils import db_get_id_no_async, db_get_data_list_no_async, db_get_table_headers_no_async
from loader import logger

logger.debug(f"{__name__} start import")

from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType
from config.config import ADMIN_ID

logger.debug(f"{__name__} finish import")

_PREFIX_ND: str = 'nrm_doc_'
_PREFIX_POZ: str = 'nrm_poz_'


def is_group(message: types.Message):
    return ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP])


def is_private(message: types.Message):
    return ChatTypeFilter(ChatType.PRIVATE)


def is_channel(message: types.Message):
    return ChatTypeFilter(ChatType.CHANNEL)


def is_sudo(message: types.Message):
    return message.from_user.id in ADMIN_ID


def filter_sub_location(message: types.Message):
    """

    :param message:
    :return:
    """
    call_data = message.data
    state = MyBot.dp.current_state(user=message.from_user.id)

    v_data: dict = asyncio.run(state.get_data())
    result = call_data in get_data_list(category_in_db='core_sublocation',
                                        category=v_data.get("main_location", None),
                                        condition='short_title')
    return result


def filter_normativedocuments(message: types.Message):
    """

    :param message:
    :return:
    """
    call_data = message.data
    state = MyBot.dp.current_state(user=message.from_user.id)

    v_data: dict = asyncio.run(state.get_data())
    result = call_data in get_data_list(category_in_db='core_normativedocuments',
                                        category=v_data.get("category", None),
                                        condition='short_title')
    return result


def get_data_list(category_in_db: str = None, category: str = None, condition: str | dict = None) -> list:
    """Функция получения данных из базы данных. При отсутствии данных поиск в json.
    При наличии condition - формирование данных согласно  condition

    :param category:
    :param category_in_db:
    :param condition:
    :return: data_list or [ ]
    """

    if not category_in_db:
        return []

    if category and condition:
        clean_datas_query: list = get_category_data_list_whits_condition(
            db_table_name=category_in_db,
            category=category,
            condition=condition
        )
        logger.debug(f'{__name__} {fanc_name()}  from db with condition: {clean_datas_query}')
        return clean_datas_query

    data_list: list = get_data_from_db(db_table_name=category_in_db)

    if not data_list:
        return []

    logger.debug(f'{__name__} {fanc_name()} {data_list = }')
    return data_list


def get_category_data_list_whits_condition(db_table_name: str, category, condition: str | dict) -> list:
    """Получение

    :param category:
    :param db_table_name: имя базы данных
    :type condition: Union[str, dict]

    """
    main_table_name: str = ''

    if db_table_name == 'core_normativedocuments':
        main_table_name = 'core_category'

    if db_table_name == 'core_sublocation':
        main_table_name = 'core_mainlocation'

    if not main_table_name:
        return []

    category_id = db_get_id_no_async(table=main_table_name, entry=category, )

    if category_id is None:
        return []

    if isinstance(condition, str):
        datas_from_db: list = get_category_data_list_whits_single_condition(
            db_table_name=db_table_name,
            item_id=category_id,
            single_condition=condition
        )

        # datas_from_db: list = add_hashtags(datas_from_db, db_table_name=db_table_name, item_id=category_id)
    #
    #     datas_from_bd: list = add_null_value_to_list(
    #         datas_from_bd, condition, db_table_name
    #     )
        return datas_from_db

    # if isinstance(condition, dict):
    #     datas_from_bd: list = get_category_data_list_whits_dict_condition(
    #         db_table_name=db_table_name,
    #         dict_condition=condition
    #     )
    #     datas_from_bd: list = add_hashtags(datas_from_bd, db_table_name=db_table_name, item_id=category_id)
    #     datas_from_bd: list = add_null_value_to_ziped_list(datas_from_bd)
    #     return datas_from_bd
    return []


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


def fanc_name() -> str:
    """Возвращает имя вызываемой функции"""
    stack = traceback.extract_stack()
    return str(stack[-2][2])
