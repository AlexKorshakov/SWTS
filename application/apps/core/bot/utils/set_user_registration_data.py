from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from app import MyBot
from apps.core.bot.utils.secondary_functions.get_filepath import preparation_registration_paths_on_pc
from loader import logger

from apps.core.bot.database.entry_in_db import entry_in_db

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.set_user_registration_data_on_google_drave import \
    set_user_registration_data_on_google_drive
from apps.core.bot.utils.json_worker.writer_json_file import write_json_reg_user_file


async def registration_data(message: types.Message, user_data):
    """
    :param message:
    :param user_data:
    :return:
    """
    user_id = message.from_user.id

    user_data = await preparation_registration_paths_on_pc(user_id=user_id, user_data=user_data)

    chat_id = message.chat.id
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Registration.user_registration)

    await set_user_registration_data(chat_id=chat_id, user_data=user_data)

    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Successfully.registration_completed)
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())


async def set_user_registration_data(*, chat_id, user_data):
    """
     :param chat_id:
     :param user_data:
     :return:
     """

    user_data = await preparation_registration_paths_on_pc(user_id=chat_id, user_data=user_data)

    if await write_json_reg_user_file(data=user_data):
        logger.info(f"Данные сохранены на pc в файл {user_data['reg_user_file']}")

    if await entry_in_db(violation_data=user_data):
        logger.info(f"Данные сохранены в local DB в файл {user_data['reg_user_file']}")

    if await set_user_registration_data_on_google_drive(chat_id=chat_id, user_data=user_data):
        logger.info(f"Данные сохранены в Google Drive в файл {user_data['reg_user_file']} \n"
                    f"https://drive.google.com/drive/folders/{user_data['parent_id']}")
