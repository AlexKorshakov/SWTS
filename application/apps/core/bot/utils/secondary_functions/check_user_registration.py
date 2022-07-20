import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app import MyBot
from apps.core.bot.utils.secondary_functions.get_filepath import get_user_registration_data_json_file
from loader import logger

from apps.core.bot.data.board_config import TempStorage
from apps.core.bot.data.category import get_data_list
from config.config import ADMIN_ID, DEVELOPER_ID
from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.secondary_functions.get_json_files import get_dirs_files, get_registered_users


async def check_user_access(*, chat_id) -> bool:
    """Проверка наличия регистрационных данных пользователя
    """

    if chat_id == int(DEVELOPER_ID):
        return True

    black_list = get_data_list("black_list")

    if chat_id in black_list:
        await user_access_fail(chat_id)
        TempStorage.user_access = False
        return False

    if TempStorage.user_access:
        return True

    _, files = await get_registered_users()

    for user_id in files:
        if user_id != str(chat_id): continue

        file_path = await get_user_registration_data_json_file(chat_id=chat_id)

        if not await check_user_registration_data_file(file_path):
            await user_access_fail(chat_id)
            return False

        await user_access_granted(user_id)
        TempStorage.user_access = True
        return True

    await user_access_fail(chat_id)
    return False


async def check_user_registration_data_file(file_path) -> bool:
    """Check"""

    if not os.path.isfile(file_path):
        return False

    file_dict: dict = await read_json_file(file_path)

    if file_dict.get('user_id'):
        return True

    return False


async def user_access_fail(chat_id):
    """Отправка сообщения о недостатке прав"""

    logger.info(f'User {chat_id} попытка доступа к функциям без регистрации')

    try:
        await MyBot.bot.send_message(chat_id=chat_id, text=f"у вас нет прав доступа \n {Messages.help_message}")
    except Exception:

        try:
            reply_markup = InlineKeyboardMarkup()
            reply_markup.add(InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}"))
            await MyBot.dp.bot.send_message(chat_id=ADMIN_ID,
                                            text=f'попытка доступа к функциям без регистрации {chat_id}',
                                            reply_markup=reply_markup)
        except Exception:

            logger.info(f'User {chat_id} ошибка уведомления ADMIN_ID')


async def user_access_granted(chat_id):
    """Отправка сообщения - доступ разрешен"""

    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}"))

    logger.info(f'доступ разрешен {chat_id}')
    await MyBot.dp.bot.send_message(chat_id=ADMIN_ID,
                                    text=f'доступ разрешен {chat_id}',
                                    reply_markup=reply_markup)


