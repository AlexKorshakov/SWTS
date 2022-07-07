from aiogram import types

from app import MyBot
from loader import logger
from pandas import DataFrame

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.generate_report.create_dataframe import create_dataframe, create_dataframe_from_data
from apps.core.bot.utils.generate_report.create_heders import create_headers
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.download_file_for_google_drive import download_files_for_google_drive
from apps.core.bot.utils.json_worker.merge_json import merge_json
from apps.core.bot.utils.json_worker.read_json_file import read_json_files
from apps.core.bot.utils.secondary_functions.get_filepath import create_file_path, get_photo_full_filepath, get_json_full_filepath, \
    get_report_full_filepath


async def get_data_report(chat_id: int, file_list: list = None):
    """Подготовка путей сохранения путей файлов и скачивание файлов из google_drive
    :param file_list:
    :param chat_id:
    :return:
    """

    # await save_merged_file_on_pc(merge_file_list)
    if not file_list:
        logger.warning('error! file_list not found!')
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

        photo_full_filepath: str = await get_photo_full_filepath(user_id=str(chat_id))
        json_full_filepath: str = await get_json_full_filepath(user_id=str(chat_id))
        report_full_filepath: str = await get_report_full_filepath(user_id=str(chat_id))

        await create_file_path(user_path=photo_full_filepath)
        await create_file_path(user_path=json_full_filepath)
        await create_file_path(user_path=report_full_filepath)

        await download_files_for_google_drive(chat_id=chat_id, file_path=json_full_filepath,
                                              photo_path=photo_full_filepath)

    dataframe = await create_dataframe(file_list=file_list)

    return dataframe


async def create_dataframe(file_list) -> DataFrame:
    """Подготовка и создание dataframe для записи в отчет
    :param file_list:
    :return:
    """
    merge_file_list = await merge_json(file_list)

    headers = await create_headers()

    data_list = await read_json_files(merge_file_list, headers)

    dataframe = await create_dataframe_from_data(data_list)

    return dataframe
