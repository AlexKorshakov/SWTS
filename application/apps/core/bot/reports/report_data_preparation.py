from __future__ import annotations

import asyncio

from loader import logger

logger.debug(f"{__name__} start import")
import datetime
from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.core.bot.bot_utils.check_user_registration import get_hse_user_data
from apps.core.bot.reports.report_data import ViolationData
from apps.core.database.db_utils import db_get_data_dict_from_table_with_id
from apps.core.utils.json_worker.writer_json_file import (write_json_file,
                                                          write_json_violation_user_file)
from apps.core.utils.secondary_functions.get_filename import get_filename_msg_with_photo
from apps.core.utils.secondary_functions.get_filepath import (create_file_path,
                                                              get_json_full_filename,
                                                              get_json_full_filepath,
                                                              get_photo_full_filename,
                                                              get_photo_full_filepath)
from apps.core.utils.secondary_functions.get_part_date import (get_day_message,
                                                               get_day_of_year_message,
                                                               get_month_message,
                                                               get_quarter_message,
                                                               get_week_message,
                                                               get_year_message)

logger.debug(f"{__name__} finish import")


async def download_photo(message: types.Message, user_id: str = None):
    """Подготовка данных предписания. первичное заполнение violation_data

    :return:
    """

    hse_user_id = message.chat.id if message else user_id

    photo_file_path = await get_photo_full_filepath(user_id=hse_user_id)
    await create_file_path(photo_file_path)

    file_id = await get_filename_msg_with_photo(message=message)
    photo_full_name = await get_photo_full_filename(user_id=hse_user_id, name=file_id)

    try:
        await message.photo[-1].download(destination_file=photo_full_name)
        return True

    except asyncio.exceptions.TimeoutError as err:
        logger.debug(f'download_photo: {hse_user_id = } {photo_full_name = } {repr(err)}')
        return False


async def preparing_violation_data(message: types.Message, state: FSMContext, chat_id: str = None, user_id: str = None):
    """Подготовка данных предписания. первичное заполнение violation_data

    :return:
    """
    violation: dict = {}
    await state.set_state(ViolationData.starting)

    hse_user_id = message.chat.id if message else user_id

    file_id = await get_filename_msg_with_photo(message=message)
    # violation_data["file_id"] = file_id
    await state.update_data(file_id=file_id)

    photo_file_path = await get_photo_full_filepath(user_id=hse_user_id)
    # violation_data["photo_file_path"] = photo_file_path
    await state.update_data(photo_file_path=photo_file_path)

    photo_full_name = await get_photo_full_filename(user_id=hse_user_id, name=file_id)
    # violation_data["photo_full_name"] = photo_full_name
    await state.update_data(photo_full_name=photo_full_name)

    json_file_path = await get_json_full_filepath(user_id=hse_user_id)
    # violation_data["json_file_path"] = json_file_path
    await state.update_data(json_file_path=json_file_path)

    json_full_name = await get_json_full_filename(user_id=hse_user_id, file_name=file_id)
    # violation_data["json_full_name"] = json_full_name
    await state.update_data(json_full_name=json_full_name)

    await create_file_path(json_file_path)
    violation[hse_user_id] = await state.get_data()
    # await write_json_violation_user_file(data=violation_data, json_full_name=json_full_name)
    await write_json_violation_user_file(data=await state.get_data(), json_full_name=json_full_name)

    await set_violation_atr_data("file_id", file_id, state=state)

    # violation_data["user_id"] = chat_id
    await state.update_data(user_id=chat_id)
    await set_violation_atr_data("user_id", user_id, state=state)

    # violation_data["violation_id"] = message.message_id
    await state.update_data(violation_id=message.message_id)
    await set_violation_atr_data("violation_id", message.message_id, state=state)

    # violation_data["user_fullname"] = message.from_user.full_name
    # # await state.update_data(user_fullname=message.from_user.full_name)
    # await set_violation_atr_data("user_fullname", message.from_user.full_name, state=state)
    #
    # violation_data["now"] = str(datetime.datetime.now())
    # # await state.update_data(now=str(datetime.datetime.now()))
    # await set_violation_atr_data("now", str(datetime.datetime.now()), state=state)
    #
    # violation_data["status"] = 'В работе'
    # await state.update_data(status='В работе')
    # await set_violation_atr_data("status", 'В работе', state=state)
    #
    # user_registration_data: dict = await get_hse_user_data(message=message)
    #
    # location = await db_get_data_dict_from_table_with_id(
    #     table_name='core_location',
    #     post_id=user_registration_data.get("hse_location", None)
    # )
    # violation_data["location"] = location['title']
    # await state.update_data(location=location['title'])
    # await set_violation_atr_data("location", location['title'], state=state)
    #
    # work_shift = await db_get_data_dict_from_table_with_id(
    #     table_name='core_workshift',
    #     post_id=user_registration_data.get("hse_work_shift", None)
    # )
    # violation_data["work_shift"] = work_shift['title']
    # await state.update_data(work_shift=work_shift['title'])
    # await set_violation_atr_data("work_shift", work_shift['title'], state=state)
    #
    # violation_data["hse_id"] = user_registration_data.get("id", None)
    # await state.update_data(hse_id=user_registration_data.get("id", None))
    # await set_violation_atr_data("hse_id", user_registration_data.get("id", None), state=state)
    #
    # violation_data["function"] = user_registration_data.get("hse_function", None)
    # await state.update_data(function=user_registration_data.get("hse_function", None))
    # await set_violation_atr_data("function", user_registration_data.get("hse_function", None), state=state)
    #
    # violation_data["name"] = user_registration_data.get("hse_full_name", None)
    # await state.update_data(name=user_registration_data.get("hse_full_name", None))
    # await set_violation_atr_data("name", user_registration_data.get("hse_full_name", None), state=state)
    #
    # violation_data["parent_id"] = user_registration_data.get("parent_id")
    # await state.update_data(parent_id=user_registration_data.get("parent_id"))
    # await set_violation_atr_data("parent_id", user_registration_data.get("parent_id"), state=state)
    #
    # violation_data["main_location"] = ''
    # await state.update_data(main_location='')
    # await set_violation_atr_data("main_location", '', state=state)
    #
    # violation_data["main_location_id"] = ''
    # await state.update_data(main_location_id='')
    # await set_violation_atr_data("main_location_id", '', state=state)
    #
    # violation_data["category"] = ''
    # await state.update_data(category='')
    # await set_violation_atr_data("category", '', state=state)
    #
    # violation_data["day"] = await get_day_message()
    # await state.update_data(day=await get_day_message())
    # await set_violation_atr_data("day", await get_day_message(), state=state)
    #
    # violation_data["week"] = await get_week_message()
    # await state.update_data(week=await get_week_message())
    # await set_violation_atr_data("week", await get_week_message(), state=state)
    #
    # violation_data["quarter"] = await get_quarter_message()
    # await state.update_data(quarter=await get_quarter_message())
    # await set_violation_atr_data("quarter", await get_quarter_message(), state=state)
    #
    # violation_data["day_of_year"] = await get_day_of_year_message()
    # await state.update_data(day_of_year=await get_day_of_year_message())
    # await set_violation_atr_data("day_of_year", await get_day_of_year_message(), state=state)
    #
    # violation_data["month"] = await get_month_message()
    # await state.update_data(month=await get_month_message())
    # await set_violation_atr_data("month", await get_month_message(), state=state)
    #
    # violation_data["year"] = await get_year_message()
    # await state.update_data(year=await get_year_message())
    # await set_violation_atr_data("year", await get_year_message(), state=state)
    #
    # deta = violation_data["day"] + ":" + violation_data["month"] + ":" + violation_data["year"]
    # violation_data["deta"] = deta
    # await state.update_data(deta=deta)
    # await set_violation_atr_data("deta", deta, state=state)

    # return violation_data


async def preparing_violations_paths_on_pc(message: types.Message, state: FSMContext, user_id: str = None):
    """Создание путей сохранения файлов и запись в json
    :param user_id:
    :param message:
    :return:
    """

    hse_user_id = message.chat.id if message else user_id

    photo_file_path = await get_photo_full_filepath(user_id=hse_user_id)
    await create_file_path(photo_file_path)

    file_id = await get_filename_msg_with_photo(message=message)
    photo_full_name = await get_photo_full_filename(user_id=hse_user_id, name=file_id)
    await message.photo[-1].download(destination_file=photo_full_name)

    photo_file_path = await get_photo_full_filepath(user_id=hse_user_id)
    # violation_data["photo_file_path"] = photo_file_path
    await state.update_data(photo_file_path=photo_file_path)

    photo_full_name = await get_photo_full_filename(user_id=hse_user_id, name=file_id)
    # violation_data["photo_full_name"] = photo_full_name
    await state.update_data(photo_full_name=photo_full_name)

    json_file_path = await get_json_full_filepath(user_id=hse_user_id)
    # violation_data["json_file_path"] = json_file_path
    await state.update_data(json_file_path=json_file_path)

    json_full_name = await get_json_full_filename(user_id=hse_user_id, file_name=file_id)
    # violation_data["json_full_name"] = json_full_name
    await state.update_data(json_full_name=json_full_name)

    await create_file_path(json_file_path)

    v_data: dict = await state.get_data()
    await write_json_violation_user_file(data=v_data)


async def preparing_violation_data_for_loading_to_google_drive(data: dict, state: FSMContext = None) -> bool:
    """Подготовка данных (id папок) на google_drive

    :rtype: dict
    """
    if not data:
        return False

    # violation_data["json_folder_id"] = data.get("json_folder_id", None)
    await state.update_data(json_folder_id=data.get("json_folder_id", None))

    # violation_data["photo_folder_id"] = data.get("photo_folder_id", None)
    await state.update_data(photo_folder_id=data.get("photo_folder_id", None))

    # violation_data["report_folder_id"] = data.get("report_folder_id", None)
    await state.update_data(report_folder_id=data.get("report_folder_id", None))

    # violation_data["parent_id"] = data.get("user_folder_id", None)
    await state.update_data(parent_id=data.get("user_folder_id", None))

    # await write_json_violation_user_file(data=violation_data)

    v_data: dict = await state.get_data()
    user_id = v_data.get('user_id')
    json_file_path = await get_json_full_filepath(user_id=user_id)
    await create_file_path(json_file_path)

    await write_json_violation_user_file(data=v_data)

    return True


async def set_violation_atr_data(atr_name: str, art_val: str | int, state: FSMContext = None, **kvargs) -> bool:
    """Запись данных  атрибута 'atr_name': art_val глобального словаря violation_data в файл json

    :param state:
    :param atr_name: str имя ключа
    :param art_val: str|int значение ключа
    :return: bool True если успешно.
    """

    logger.debug(f'set_violation_atr_data: {atr_name = } {art_val = }')

    if not atr_name:
        return False

    # violation_data[atr_name] = art_val
    # await write_json_file(data=violation_data, json_full_name=violation_data["json_full_name"])
    await state.update_data({atr_name: art_val})

    user_dict: dict = await state.get_data()
    json_full_name = user_dict["json_full_name"]
    await write_json_file(data=user_dict, name=json_full_name)
    return True

# def get_vio_atr_data(atr_name: str):
#     """
#
#     :param atr_name:
#     :return:
#     """
#     pprint(f'{ violation_data = }')
#     pprint(f'get_violation_atr_data: {atr_name = } {violation_data.get[atr_name, None]}')
#
#     logger.info(f'get_violation_atr_data: {atr_name = } {violation_data.get[atr_name, None]}')
#     return violation_data.get[atr_name, None]
