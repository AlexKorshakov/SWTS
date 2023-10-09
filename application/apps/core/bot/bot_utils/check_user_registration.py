from __future__ import print_function
from __future__ import annotations

from pandas import DataFrame

from apps.core.bot.bot_utils.check_access import base_check_user_access
from apps.core.database.query_constructor import QueryConstructor
from loader import logger

logger.debug(f"{__name__} start import")

import asyncio
import re
from pprint import pprint
from aiogram import types

from apps.MyBot import bot_send_message
from apps.core.bot.messages.messages_test import msg
from apps.core.bot.messages.messages import Messages
from apps.core.bot.bot_utils.bot_admin_notify import admin_notify
from apps.core.database.db_utils import db_get_table_headers, db_get_data_list

logger.debug(f"{__name__} finish import")


async def get_list_table_headers() -> list:
    """Получение заголовков таблицы db_table_name

    :return:
    """
    db_table_name: str = 'core_hseuser'
    table_headers: list = [item[1] for item in await db_get_table_headers(table_name=db_table_name)]
    return table_headers


async def get_list_table_values(chat_id: int) -> list:
    """Получение данных таблицы по chat_id

    :param chat_id:
    :return:
    """

    query_kwargs: dict = {
        "action": 'SELECT', "subject": '*',
        "conditions": {
            "hse_telegram_id": chat_id,
        },
    }
    query: str = await QueryConstructor(None, 'core_hseuser', **query_kwargs).prepare_data()
    datas_query: list = await db_get_data_list(query=query)

    if not datas_query:
        return []
    if not isinstance(datas_query, list):
        return []

    return list(datas_query[0])


async def get_data_dict(table_headers: list, table_data: list) -> dict:
    """Формирование dict с данными

    :param table_headers:
    :param table_data:
    :return:
    """
    table_dict: dict = {}
    for header, data in zip(table_headers, table_data):
        table_dict[header] = data

    return table_dict


async def get_hse_role(hse_user_data_dict: dict) -> list:
    """Получение ролей пользователя из БД на основе chat_id

    :param hse_user_data_dict:
    :return: list
    """

    hse_role_name: list = [name for name, value in hse_user_data_dict.items() if re.search(r'_role_', name)]
    return hse_role_name


async def get_dict_hse_user_role(hse_user_data_dict: dict) -> dict:
    """Получение ролей пользователя из БД на основе chat_id

    :return: dict
    """

    hse_roles: list = await get_hse_role(hse_user_data_dict)
    hse_roles_dict = {name: value for name, value in hse_user_data_dict.items() if name in hse_roles}
    return dict(hse_roles_dict)


async def get_hse_user_data(*, message: types.Message = None, chat_id: int | str = None) -> dict:
    """Получение данных пользователя из БД на основе chat_id

    :return: dict
    """
    chat_id = chat_id if chat_id else message.chat.id

    table_data: list = await get_list_table_values(chat_id)
    if not table_data:
        return {}

    table_headers: list = await get_list_table_headers()
    hse_user_data_dict: dict = await get_data_dict(table_headers, table_data)

    if not hse_user_data_dict:
        return {}

    return hse_user_data_dict


async def check_user_access(*, chat_id, message: types.Message = None, notify_admin: bool = None,
                            role_df: DataFrame = None) -> bool:
    """Проверка наличия регистрационных данных пользователя

    :return: bool
    """

    chat_id = chat_id if chat_id else message.chat.id

    if not await base_check_user_access(chat_id, role_df=role_df):
        logger.error(f'access fail {chat_id = }')
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    table_data: list = await get_list_table_values(chat_id)
    if not table_data:
        logger.error(f'access fail {chat_id = } {table_data =}')
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    table_headers: list = await get_list_table_headers()
    hse_user_data_dict: dict = await get_data_dict(table_headers, table_data)

    if not hse_user_data_dict:
        logger.error(f'access fail {chat_id = } {hse_user_data_dict =}')
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    if not hse_user_data_dict.get('hse_is_work', None):
        logger.error(
            f"access fail {chat_id = } {hse_user_data_dict =} hse_is_work {hse_user_data_dict.get('hse_is_work', None)}")
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    if not hse_user_data_dict.get('hse_status', None):
        logger.error(
            f"access fail {chat_id = } {hse_user_data_dict =} hse_status {hse_user_data_dict.get('hse_status', None)}")
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    hse_user_role_dict: dict = await get_dict_hse_user_role(hse_user_data_dict)
    logger.debug(f'{chat_id = } ::: {hse_user_role_dict = }')

    if not hse_user_role_dict.get('hse_role_is_user', None):
        logger.info(f"{chat_id = } ::: {hse_user_role_dict.get('hse_role_is_user', None) = }")
        logger.error(
            f"access fail {chat_id = } {hse_user_role_dict =} hse_status {hse_user_role_dict.get('hse_role_is_user', None)}")
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    if notify_admin:
        logger.info(f"{notify_admin = }")
        await user_access_granted(chat_id)

    return True


async def user_access_fail(chat_id: int, notify_text: str = None, hse_id: str = None):
    """Отправка сообщения о недостатке прав
    """
    hse_id = hse_id if hse_id else chat_id

    try:
        default_answer_text: str = 'У вас нет прав доступа \n По всем вопросам обращайтесь к администратору\n' \
                                   'https://t.me/AlexKor_MSK \n\n'

        part_1 = f"{await msg(hse_id, cat='error', msge='access_fail', default=default_answer_text).g_mas()}"
        part_2 = f"{await msg(hse_id, cat='help', msge='help_message', default=Messages.help_message).g_mas()}"
        answer_text = f'{part_1}\n\n{part_2}'
        print(f'{answer_text = }')

        await bot_send_message(chat_id=chat_id, text=answer_text, disable_web_page_preview=True)
        return

    except Exception as err:
        logger.error(f'User {chat_id} ошибка уведомления пользователя {repr(err)}')
        await admin_notify(user_id=chat_id, notify_text=notify_text)

    finally:
        if not notify_text:
            notify_text: str = f'User {chat_id} попытка доступа к функциям без регистрации'

        logger.error(notify_text)
        # button = types.InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}")
        await admin_notify(
            user_id=chat_id, notify_text=notify_text,
            # button=button
        )


async def user_access_granted(chat_id: int):
    """Отправка сообщения - доступ разрешен"""

    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}"))

    logger.debug(f'доступ разрешен {chat_id}')
    await admin_notify(user_id=chat_id, notify_text=f'доступ разрешен {chat_id}')


async def get_user_data_dict(chat_id: int) -> tuple[dict, dict]:
    """Получение данных пользователя и ролей пользователя отдельно

    :param chat_id:
    :return: tuple[dict, dict]
    """

    table_data: list = await get_list_table_values(chat_id)
    table_headers: list = await get_list_table_headers()
    hse_user_data_dict: dict = await get_data_dict(table_headers, table_data)
    hse_user_role_dict: dict = await get_dict_hse_user_role(hse_user_data_dict)

    return hse_user_data_dict, hse_user_role_dict


async def test2():
    chat_id = '373084462'
    user_access: bool = await check_user_access(chat_id=chat_id)

    pprint(f"{user_access = }")


if __name__ == "__main__":
    asyncio.run(test2())
