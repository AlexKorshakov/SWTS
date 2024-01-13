from __future__ import annotations

from loader import logger

logger.debug(f"{__name__} start import")

import asyncio
from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType
from pandas import DataFrame
import traceback
from apps.MyBot import MyBot
from apps.core.bot.bot_utils.check_access import (user_access_fail,
                                                  get_id_list,
                                                  user_access_granted)
from apps.core.database.query_constructor import QueryConstructor
from apps.core.database.db_utils import (db_get_data_list_no_async,
                                         db_get_id,
                                         db_get_data_list,
                                         db_get_clean_headers)

logger.debug(f"{__name__} finish import")

_PREFIX_ND: str = 'nrm_doc_'
_PREFIX_POZ: str = 'nrm_poz_'


async def is_admin_user_actions(call: types.CallbackQuery):
    return True if 'admin_user_actions_' in call.data else False


async def is_admin_add_user(call: types.CallbackQuery):
    return True if 'admin_add_user_' in call.data else False


async def is_admin_add_user_progress(call: types.CallbackQuery):
    return True if 'admin_add_add_user_progress_' in call.data else False


async def admin_add_user_default(call: types.CallbackQuery):
    return True if 'admin_add_add_user_default_' in call.data else False


async def admin_add_user_role_item(call: types.CallbackQuery):
    return True if 'admin_add_add_user_role_item_' in call.data else False


async def admin_add_user_stop(call: types.CallbackQuery):
    return True if 'admin_add_add_user_stop' in call.data else False


async def admin_add_user_role_update_role(call: types.CallbackQuery):
    return True if 'hse_role_item_' in call.data else False


async def is_lna_text_answer(call: types.CallbackQuery):
    return True if '_lna_file_' in call.data else False


# async def is_group(message: types.Message):
#     return ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP])


async def is_private(message: types.Message):
    return ChatTypeFilter(ChatType.PRIVATE)


async def is_channel(message: types.Message):
    return ChatTypeFilter(ChatType.CHANNEL)


# async def is_sudo(message: types.Message) -> str | int:
#     return message.from_user.id in ADMIN_ID


async def filter_sub_location(message: types.Message):
    """

    :param message:
    :return:
    """
    call_data = message.data
    state = MyBot.dp.current_state(user=message.from_user.id)

    v_data: dict = asyncio.run(state.get_data())
    result = call_data in await get_data_list(category_in_db='core_sublocation',
                                              category=v_data.get("main_location", None),
                                              condition='short_title')
    return result


async def filter_normativedocuments(message: types.Message):
    """

    :param message:
    :return:
    """
    call_data = message.data
    state = MyBot.dp.current_state(user=message.from_user.id)

    v_data: dict = asyncio.run(state.get_data())
    result = call_data in await get_data_list(category_in_db='core_normativedocuments',
                                              category=v_data.get("category", None),
                                              condition='short_title')
    return result


async def filter_is_super_user(message: types.Message):
    """

    :param message:
    :return:
    """
    user = message.from_user.id

    result = await check_super_user_access(chat_id=user)
    logger.info(f'check_super_user_access {user = } {result = }')
    return result


async def check_super_user_access(chat_id: int | str, role_df: DataFrame = None) -> bool:
    """

    :param role_df:
    :param chat_id:
    :return:
    """
    super_user_id_list: list = await get_id_list(
        hse_user_id=chat_id, user_role='hse_role_is_super_user', hse_role_df=role_df
    )
    if not super_user_id_list:
        logger.error(f'{await fanc_name()} access fail {chat_id = }')
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    if chat_id not in super_user_id_list:
        logger.error(f'{await fanc_name()} access fail {chat_id = }')
        return False

    logger.info(f"user_access_granted for {chat_id = }")
    await user_access_granted(chat_id, role=await fanc_name())
    return True


async def get_data_list(category_in_db: str = None, category: str = None, condition: str | dict = None) -> list:
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
        clean_datas_query: list = await get_category_data_list_whits_condition(
            db_table_name=category_in_db,
            category=category,
            condition=condition
        )
        logger.debug(f'{__name__} {await fanc_name()}  from db with condition: {clean_datas_query}')
        return clean_datas_query

    data_list: list = await get_data_from_db(db_table_name=category_in_db)

    if not data_list:
        return []

    logger.debug(f'{__name__} {await fanc_name()} {data_list = }')
    return data_list


async def get_category_data_list_whits_condition(db_table_name: str, category: str, condition: str | dict) -> list:
    """Получение

    :param category:
    :param condition:
    :param db_table_name: имя базы данных
    """
    main_table_name: str = ''

    if db_table_name == 'core_normativedocuments':
        main_table_name = 'core_category'

    if db_table_name == 'core_sublocation':
        main_table_name = 'core_mainlocation'

    if not main_table_name:
        return []

    category_id: int = await db_get_id(table=main_table_name, entry=category, calling_function_name=await fanc_name())

    if category_id is None:
        return []

    if isinstance(condition, str):
        datas_from_db: list = await get_category_data_list_whits_single_condition(
            db_table_name=db_table_name,
            item_id=category_id,
            single_condition=condition
        )
        return datas_from_db

    return []


async def get_category_data_list_whits_single_condition(db_table_name: str, item_id: int,
                                                        single_condition: str) -> list:
    """ Получение данных если single_condition

    :param single_condition:
    :param item_id:
    :param db_table_name: имя базы данных
    :return: list
    """
    clean_datas_query: list = []
    query: str = ""

    if db_table_name == 'core_sublocation':
        query_kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "main_location_id": item_id,
            },
        }
        query: str = await QueryConstructor(None, db_table_name, **query_kwargs).prepare_data()

        logger.debug(f'{__name__} {await fanc_name()} {query = }')

    if db_table_name == 'core_normativedocuments':
        query_kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "category_id": item_id,
            },
        }
        query: str = await QueryConstructor(None, db_table_name, **query_kwargs).prepare_data()

        logger.debug(f'{__name__} {await fanc_name()} {query = }')

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


async def get_data_from_db(db_table_name: str) -> list:
    """Получение
    """
    query_kwargs: dict = {
        "action": 'SELECT', "subject": '*',
    }

    query: str = await QueryConstructor(None, db_table_name, **query_kwargs).prepare_data()

    datas_query: list = await db_get_data_list(query=query)
    clean_headers: list = await db_get_clean_headers(table_name=db_table_name)

    if not isinstance(datas_query, list):
        return []

    if 'short_title' in clean_headers:
        data_list = [data[2] for data in datas_query]
        return data_list

    if datas_query:
        logger.debug(f'retrieved data from database: {datas_query}')
        data_list = [data[1] for data in datas_query]
        return data_list

    return []


async def fanc_name() -> str:
    """Возвращает имя вызываемой функции"""
    stack = traceback.extract_stack()
    return str(stack[-2][2])
