import asyncio
import os
import re

from aiogram import types
from datetime import datetime
from pprint import pprint

# from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.messages.messages import Messages
from apps.core.utils.bot_utils_processor.notify_admins import admin_notify
from apps.core.utils.json_worker.read_json_file import read_json_file
from config.config import ADMIN_ID
from loader import logger


async def get_list_table_headers() -> list:
    """Получение заголовков таблицы db_table_name

    :return:
    """
    db_table_name: str = 'core_hseuser'
    table_headers: list = [item[1] for item in DataBase().get_table_headers(table_name=db_table_name)]
    return table_headers


async def get_list_table_values(chat_id: str) -> list:
    """Получение данных таблицы по chat_id

    :param chat_id:
    :return:
    """

    db_table_name: str = 'core_hseuser'
    query: str = f'SELECT * FROM `{db_table_name}` WHERE `hse_telegram_id` = {chat_id}'
    datas_query: list = DataBase().get_data_list(query=query)

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
    """

    :param hse_user_data_dict:
    :return:
    """

    hse_role_name: list = [name for name, value in hse_user_data_dict.items() if re.search(r'_role_', name)]
    return hse_role_name


async def get_dict_hse_user_role(hse_user_data_dict: dict) -> dict:
    """
    """

    hse_roles: list = await get_hse_role(hse_user_data_dict)
    hse_roles_dict = {name: value for name, value in hse_user_data_dict.items() if name in hse_roles}
    return dict(hse_roles_dict)


async def get_hse_user_data(*, message: types.Message = None) -> dict:
    """

    :return:
    """

    chat_id = message.chat.id

    table_data: list = await get_list_table_values(chat_id)
    if not table_data:
        return {}

    table_headers: list = await get_list_table_headers()
    hse_user_data_dict: dict = await get_data_dict(table_headers, table_data)

    if not hse_user_data_dict:
        return {}

    return hse_user_data_dict


async def check_user_access(*, chat_id, message: types.Message = None, notify_admin: bool = None) -> bool:
    """Проверка наличия регистрационных данных пользователя
    """

    if message:
        chat_id = message.chat.id

    table_data: list = await get_list_table_values(chat_id)
    if not table_data:
        await user_access_fail(message)
        return False

    table_headers: list = await get_list_table_headers()
    hse_user_data_dict: dict = await get_data_dict(table_headers, table_data)
    pprint(f'{hse_user_data_dict = }')
    if not hse_user_data_dict:
        await user_access_fail(message)
        return False

    if not hse_user_data_dict.get('hse_is_work', None):
        await user_access_fail(message)
        return False

    if not hse_user_data_dict.get('hse_status', None):
        await user_access_fail(message)
        return False

    hse_user_role_dict: dict = await get_dict_hse_user_role(hse_user_data_dict)
    pprint(f'{hse_user_role_dict = }')

    if not hse_user_role_dict.get('hse_role_is_user', None):
        await user_access_fail(message)
        return False

    if notify_admin:
        await user_access_granted(chat_id)

    return True


async def check_user_registration_data_file(file_path) -> bool:
    """Check"""

    if not os.path.isfile(file_path):
        return False

    file_dict: dict = await read_json_file(file_path)

    if file_dict.get('user_id'):
        return True

    return False


async def user_access_fail(message: types.Message, notify_text: str = None):
    """Отправка сообщения о недостатке прав"""

    chat_id = message.chat.id

    if not notify_text:
        notify_text: str = f'User {chat_id} попытка доступа к функциям без регистрации'
    logger.info(notify_text)

    await admin_notify(user_id=chat_id, notify_text=notify_text)
    try:
        await message.answer(
            text=f'У вас нет прав доступа \n {Messages.help_message}!\n'
                 f'По всем вопросам обращайтесь к администратору\n'
                 f'https://t.me/AlexKor_MSK',
            disable_web_page_preview=True)
        return

    except Exception as err:
        logger.error(f'User {chat_id} ошибка уведомления пользователя {repr(err)}')

        try:
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(
                types.InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}")
            )
            # await MyBot.dp.bot.send_message(chat_id=ADMIN_ID,
            #                                 text=notify_text,
            #                                 reply_markup=reply_markup)
        except Exception as err:
            logger.error(f'User {chat_id} ошибка уведомления ADMIN_ID {repr(err)}')


async def user_access_granted(chat_id):
    """Отправка сообщения - доступ разрешен"""

    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}"))

    logger.info(f'доступ разрешен {chat_id}')
    # await MyBot.dp.bot.send_message(chat_id=ADMIN_ID,
    #                                 text=f'доступ разрешен {chat_id}',
    #                                 reply_markup=reply_markup)


async def test2():
    chat_id = '373084462'
    answer: bool = await check_user_access(chat_id=chat_id)

    pprint(answer)


if __name__ == "__main__":
    asyncio.run(test2())
