from loader import logger

logger.debug(f"{__name__} start import")
import datetime
from pprint import pprint

from aiogram import types
from apps.core.bot.bot_utils.check_user_registration import get_hse_user_data
from apps.core.bot.reports.report_data import violation_data
from apps.core.database.db_utils import db_get_data_dict_from_table_with_id
from apps.core.utils.json_worker.writer_json_file import (
    write_json_file, write_json_violation_user_file)
from apps.core.utils.secondary_functions.get_filename import \
    get_filename_msg_with_photo
from apps.core.utils.secondary_functions.get_filepath import (
    create_file_path, get_json_full_filename, get_json_full_filepath,
    get_photo_full_filename, get_photo_full_filepath)
from apps.core.utils.secondary_functions.get_part_date import (
    get_day_message, get_day_of_year_message, get_month_message,
    get_quarter_message, get_week_message, get_year_message)

logger.debug(f"{__name__} finish import")


async def preparing_violation_data(message: types.Message, chat_id: str):
    """Подготовка данных предписания. первичное заполнение violation_data

    :return:
    """

    violation_data["file_id"] = await get_filename_msg_with_photo(message)

    violation_data["user_id"] = chat_id
    violation_data["violation_id"] = message.message_id
    violation_data["user_fullname"] = message.from_user.full_name

    violation_data["now"] = str(datetime.datetime.now())

    violation_data["status"] = 'В работе'

    user_registration_data: dict = await get_hse_user_data(message=message)

    location = await db_get_data_dict_from_table_with_id(
        table_name='core_location',
        post_id=user_registration_data.get("hse_location", None)
    )
    violation_data["location"] = location['title']

    work_shift = await db_get_data_dict_from_table_with_id(
        table_name='core_workshift',
        post_id=user_registration_data.get("hse_work_shift", None)
    )
    violation_data["work_shift"] = work_shift['title']

    violation_data["hse_id"] = user_registration_data.get("id", None)

    violation_data["function"] = user_registration_data.get("hse_function", None)
    violation_data["name"] = user_registration_data.get("hse_full_name", None)
    violation_data["parent_id"] = user_registration_data.get("parent_id")

    violation_data["main_location"] = ''
    violation_data["main_location_id"] = ''
    violation_data["category"] = ''

    violation_data["day"] = await get_day_message()
    violation_data["week"] = await get_week_message()
    violation_data["quarter"] = await get_quarter_message()
    violation_data["day_of_year"] = await get_day_of_year_message()
    violation_data["month"] = await get_month_message()
    violation_data["year"] = await get_year_message()
    violation_data["data"] = violation_data["day"] + ":" + violation_data["month"] + ":" + violation_data["year"]

    violation_data["photo_file_path"] = await get_photo_full_filepath(user_id=violation_data["user_id"])
    violation_data["photo_full_name"] = await get_photo_full_filename(user_id=violation_data["user_id"],
                                                                      name=violation_data["file_id"])
    await create_file_path(violation_data["photo_file_path"])
    await message.photo[-1].download(destination=violation_data["photo_full_name"], make_dirs=False)

    violation_data["json_file_path"] = await get_json_full_filepath(user_id=violation_data["user_id"])
    violation_data["json_full_name"] = await get_json_full_filename(user_id=violation_data["user_id"],
                                                                    file_name=violation_data["file_id"])
    await create_file_path(violation_data["json_file_path"])

    await write_json_violation_user_file(data=violation_data)

    return violation_data


async def preparing_violations_paths_on_pc(message: types.Message):
    """Создание путей сохранения файлов и запись в json
    :param message:
    :return:
    """
    violation_data["photo_file_path"] = await get_photo_full_filepath(user_id=violation_data["user_id"])
    violation_data["photo_full_name"] = await get_photo_full_filename(user_id=violation_data["user_id"],
                                                                      name=violation_data["file_id"])
    await create_file_path(violation_data["photo_file_path"])
    await message.photo[-1].download(destination=violation_data["photo_full_name"], make_dirs=False)

    violation_data["json_file_path"] = await get_json_full_filepath(user_id=violation_data["user_id"])
    violation_data["json_full_name"] = await get_json_full_filename(user_id=violation_data["user_id"],
                                                                    file_name=violation_data["file_id"])
    await create_file_path(violation_data["json_file_path"])

    await write_json_violation_user_file(data=violation_data)


async def preparing_violation_data_for_loading_to_google_drive(data: dict) -> bool:
    """Подготовка данных (id папок) на google_drive

    :rtype: dict
    """
    if not data:
        return False

    violation_data["json_folder_id"] = data.get("json_folder_id", None)
    violation_data["photo_folder_id"] = data.get("photo_folder_id", None)
    violation_data["report_folder_id"] = data.get("report_folder_id", None)
    violation_data["parent_id"] = data.get("user_folder_id", None)

    await write_json_violation_user_file(data=violation_data)

    return True


async def set_violation_atr_data(atr_name, art_val, **kvargs):
    """

    :param atr_name:
    :param art_val:
    :return:
    """

    pprint(f'set_violation_atr_data: {atr_name = } {art_val = }')
    logger.debug(f'set_violation_atr_data: {atr_name = } {art_val = }')

    if atr_name:
        violation_data[atr_name] = art_val
        await write_json_file(data=violation_data, name=violation_data["json_full_name"])


def get_vio_atr_data(atr_name: str):
    """

    :param atr_name:
    :return:
    """
    pprint(f'{ violation_data = }')
    pprint(f'get_violation_atr_data: {atr_name = } {violation_data.get[atr_name, None]}')

    logger.info(f'get_violation_atr_data: {atr_name = } {violation_data.get[atr_name, None]}')
    return violation_data.get[atr_name, None]
