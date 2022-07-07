from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from app import MyBot
from loader import logger

import apps.core.bot.data.board_config
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.database.entry_in_db import entry_in_db

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.del_messege import cyclical_deletion_message
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    set_user_violation_data_on_google_drive
from apps.core.bot.utils.json_worker.writer_json_file import write_json_violation_user_file


async def pre_set_violation_data(message: types.Message):
    """Интерфейс записи нарушения на Google Drive
    """
    chat_id = message.from_user.id
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.begin)

    stop_violation_id = apps.core.bot.data.board_config.stop_violation_mes_id = message.message_id + 3
    logger.info(f"start_violation message.from_user.id {stop_violation_id}")

    await set_violation_data(chat_id=chat_id)

    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.completed_successfully)
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())

    await cyclical_deletion_message(chat_id=chat_id)


async def set_violation_data(*, chat_id):
    """запись нарушения на Google Drive
    """
    if await write_json_violation_user_file(data=violation_data):
        logger.info(f"Данные сохранены на pc в файл {violation_data['json_full_name']}")

    if await set_user_violation_data_on_google_drive(chat_id=chat_id, violation_data=violation_data):
        logger.info(f"Данные сохранены в Google Drive в директорию \n"
                    f"https://drive.google.com/drive/folders/{violation_data['json_folder_id']}")

    if await entry_in_db(violation_data=violation_data):
        logger.info(f"Данные сохранены в local DB в файл {violation_data['json_full_name']}")
