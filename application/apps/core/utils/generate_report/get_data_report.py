from apps.core.bot.messages.messages import Messages
from apps.core.utils.generate_report.create_dataframe import \
    create_dataframe_from_data
from apps.core.utils.generate_report.create_heders import create_headers
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.download_file_for_google_drive import \
    upload_files_from_google_drive
from apps.core.utils.json_worker.merge_json import merge_json
from apps.core.utils.json_worker.read_json_file import read_json_files
from apps.core.utils.secondary_functions.get_filepath import (
    create_file_path, get_json_full_filepath, get_photo_full_filepath,
    get_report_full_filepath)
from apps.MyBot import bot_send_message
from loader import logger
from pandas import DataFrame


async def get_data_report(chat_id: int, file_list: list = None):
    """Подготовка путей сохранения путей файлов и скачивание файлов из google_drive

    :param file_list:
    :param chat_id:
    :return:
    """

    # await save_merged_file_on_pc(merge_file_list)
    if not file_list:
        logger.warning('error! file_list not found!')
        await bot_send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

        photo_full_filepath: str = await get_photo_full_filepath(user_id=str(chat_id))
        json_full_filepath: str = await get_json_full_filepath(user_id=str(chat_id))
        report_full_filepath: str = await get_report_full_filepath(user_id=str(chat_id))

        await create_file_path(path=photo_full_filepath)
        await create_file_path(path=json_full_filepath)
        await create_file_path(path=report_full_filepath)

        await upload_files_from_google_drive(
            chat_id=chat_id, file_path=json_full_filepath, photo_path=photo_full_filepath)

    dataframe = await create_dataframe(file_list=file_list)

    return dataframe


async def create_dataframe(file_list: list) -> DataFrame:
    """Подготовка и создание dataframe для записи в отчет

    :param file_list: list с файлами для создания dataframe
    :return: dataframe
    """
    merge_file_list: list = await merge_json(file_list)

    headers: list = await create_headers()

    data_list: list = await read_json_files(files=merge_file_list, data=headers)

    dataframe: DataFrame = await create_dataframe_from_data(data=data_list)

    return dataframe
