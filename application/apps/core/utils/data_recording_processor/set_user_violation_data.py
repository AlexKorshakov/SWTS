from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.reports.report_data_preparation import preparing_violation_data_for_loading_to_google_drive
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import \
    drive_account_auth_with_oauth2client
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.get_folder_id import \
    get_folders_ids_from_google_drive
from loader import logger

import apps.core.bot.data.board_config
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.database.entry_in_db import write_data_in_database

from apps.core.bot.messages.messages import Messages
from apps.core.utils.bot_utils_processor.del_messege import cyclical_deletion_message
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    write_violation_data_on_google_drive
from apps.core.utils.json_worker.writer_json_file import write_json_violation_user_file


async def pre_set_violation_data(message: types.Message):
    """Интерфейс записи нарушения на Google Drive

    """
    chat_id = message.from_user.id
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.begin)

    stop_violation_id = apps.core.bot.data.board_config.stop_violation_mes_id = message.message_id + 3
    logger.info(f"start_violation message.from_user.id {stop_violation_id}")

    drive_service = await drive_account_auth_with_oauth2client()
    data: dict = await get_folders_ids_from_google_drive(user=chat_id, drive_service=drive_service)

    if not await preparing_violation_data_for_loading_to_google_drive(data=data):
        return False

    await set_violation_data(chat_id=chat_id)

    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.completed_successfully)
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())

    await cyclical_deletion_message(chat_id=chat_id)


async def set_violation_data(*, chat_id: str):
    """Запись и сохранение данных в local storage, database, Google Drive
    """

    if await write_json_violation_user_file(data=violation_data):
        logger.info(f"Данные сохранены в local storage {violation_data['json_full_name']}")

    if await write_violation_data_on_google_drive(chat_id=chat_id, violation_data=violation_data):
        logger.info(f"Данные сохранены в Google Drive в директорию \n"
                    f"https://drive.google.com/drive/folders/{violation_data['json_folder_id']}")

    if await write_data_in_database(violation_data=violation_data):
        logger.info(f"Данные сохранены в database в файл {DataBase().db_file}")
