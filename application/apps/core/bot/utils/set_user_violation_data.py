from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.get_folder_id import get_root_folder_id, get_user_folder_id, \
    get_json_folder_id, get_photo_folder_id, get_report_folder_id
from apps.core.bot.utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from loader import logger

import apps.core.bot.data.board_config
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.database.entry_in_db import write_data_in_database

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.del_messege import cyclical_deletion_message
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    write_violation_data_on_google_drive, JSON_FOLDER_NAME, PHOTO_FOLDER_NAME, REPORT_FOLDER_NAME
from apps.core.bot.utils.json_worker.writer_json_file import write_json_violation_user_file


async def pre_set_violation_data(message: types.Message):
    """Интерфейс записи нарушения на Google Drive
    """
    chat_id = message.from_user.id
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.begin)

    stop_violation_id = apps.core.bot.data.board_config.stop_violation_mes_id = message.message_id + 3
    logger.info(f"start_violation message.from_user.id {stop_violation_id}")

    if not await preparing_data_for_loading(user=chat_id):
        return False

    await set_violation_data(chat_id=chat_id)

    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.completed_successfully)
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())

    await cyclical_deletion_message(chat_id=chat_id)


async def preparing_data_for_loading(user: str, drive_service: object = None) -> dict:
    """ Получение id основных папок для chat_id для загрузки в облачный репозиторий

    Подготовка данных к загрузке на Google Drive

    Дополнение violation_data

    :param user: id пользователя
    :param drive_service: объект авторизации

    :return: {'user_folder_id', 'json_folder_id', 'photo_folder_id', 'report_folder_id',} or {}
    """
    if not drive_service: drive_service = await drive_account_auth_with_oauth2client()

    if not drive_service:
        logger.error(f"drive_service is empty {drive_service = }")
        return {}

    root_folder_id = await get_root_folder_id(drive_service=drive_service,
                                              root_folder_name=ROOT_REPORT_FOLDER_NAME)
    if not root_folder_id:
        return {}

    user_folder_id = await get_user_folder_id(drive_service=drive_service,
                                              root_folder_name=str(user),
                                              parent_id=root_folder_id, )

    json_folder_id = await get_json_folder_id(drive_service=drive_service,
                                              json_folder_name=JSON_FOLDER_NAME,
                                              parent_id=user_folder_id,
                                              root_json_folder_id=user_folder_id)

    photo_folder_id = await get_photo_folder_id(drive_service=drive_service,
                                                photo_folder_name=PHOTO_FOLDER_NAME,
                                                parent_id=user_folder_id,
                                                root_photo_folder_id=user_folder_id)

    report_folder_id = await get_report_folder_id(drive_service=drive_service,
                                                  report_folder_name=REPORT_FOLDER_NAME,
                                                  parent_id=user_folder_id,
                                                  root_report_folder_id=user_folder_id)

    if not json_folder_id:
        return {}

    violation_data["json_folder_id"] = json_folder_id
    violation_data["photo_folder_id"] = photo_folder_id
    violation_data["report_folder_id"] = report_folder_id
    violation_data["parent_id"] = user_folder_id

    return {
        'json_folder_id': json_folder_id,
        'photo_folder_id': photo_folder_id,
        'report_folder_id': report_folder_id,
        'user_folder_id': user_folder_id
    }


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
