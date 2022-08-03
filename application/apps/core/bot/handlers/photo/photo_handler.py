import datetime

from aiogram import types

from app import MyBot
from loader import logger

from apps.core.bot.data import board_config

from apps.core.bot.data.report_data import violation_data

from apps.core.bot.utils.goolgedrive.googledrive_worker import write_data_on_google_drive
from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.misc import rate_limit
from apps.core.bot.utils.secondary_functions.get_part_date import get_day_message, get_month_message, get_year_message
from apps.core.bot.utils.secondary_functions.get_filename import get_filename_msg_with_photo
from apps.core.bot.utils.secondary_functions.get_filepath import preparation_violations_paths_on_pc, \
    get_user_registration_data_json_file
from apps.core.bot.utils.select_start_category import select_start_category
from apps.core.bot.utils.secondary_functions.check_user_registration import check_user_access

WORK_ON_HEROKU = False
WORK_ON_PC = True

logger.debug("message_handler 'photo'")


@rate_limit(limit=5)
@MyBot.dp.message_handler(content_types=["photo"])
async def photo_handler(message: types.Message):
    """Обработчик сообщений с фото
    """
    # if await photo_processing(message):
    #     return

    chat_id = message.chat.id
    logger.info(f"{chat_id = }")
    if not await check_user_access(chat_id=chat_id):
        return

    logger.info("photo_handler get photo")
    start_violation = board_config.start_violation_mes_id = message.message_id
    logger.info(f"start_violation message.from_user.id {start_violation}")

    violation_data["file_id"] = await get_filename_msg_with_photo(message)

    violation_data["user_id"] = chat_id
    violation_data["violation_id"] = message.message_id
    violation_data["user_fullname"] = message.from_user.full_name

    violation_data["now"] = str(datetime.datetime.now())

    violation_data["status"] = 'В работе'

    violation_data["day"] = await get_day_message()
    violation_data["month"] = await get_month_message()
    violation_data["year"] = await get_year_message()
    violation_data["data"] = violation_data["day"] + ":" + violation_data["month"] + ":" + violation_data["year"]

    user_registration_data = await read_json_file(
        file=await get_user_registration_data_json_file(chat_id=chat_id))

    violation_data["location"] = user_registration_data.get("name_location")
    violation_data["work_shift"] = user_registration_data.get("work_shift")
    violation_data["function"] = user_registration_data.get("function")
    violation_data["name"] = user_registration_data.get("name")
    violation_data["parent_id"] = user_registration_data.get("parent_id")

    if WORK_ON_HEROKU:
        await write_data_on_google_drive(message)
        return

    if WORK_ON_PC:
        await preparation_violations_paths_on_pc(message)

    await select_start_category(message)
