from apps.core.bot.handlers.photo.qr_photo_processing import qr_code_processing
from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.reports.report_data_preparation import \
    preparing_violation_data
from apps.core.bot.bot_utils.select_start_category import \
    select_start_category
from apps.core.utils.goolgedrive_processor.googledrive_worker import \
    write_data_on_google_drive
from apps.core.utils.misc import rate_limit
from apps.MyBot import MyBot
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE

logger.debug(f"{__name__} finish import")

WORK_ON_HEROKU = False
WORK_ON_PC = True

logger.debug("message_handler 'photo'")


@rate_limit(limit=5)
@MyBot.dp.message_handler(content_types=["photo"])
async def photo_handler(message: types.Message):
    """Обработчик сообщений с фото
    """

    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    if await qr_code_processing(message):
        return

    logger.info("photo_handler get photo")

    start_violation = board_config.start_violation_mes_id = message.message_id

    logger.info(f"start_violation message.from_user.id {start_violation}")

    await preparing_violation_data(message=message, chat_id=chat_id)

    if WORK_ON_HEROKU and WRITE_DATA_ON_GOOGLE_DRIVE:
        await write_data_on_google_drive(message)
        return

    # if WORK_ON_PC:
    #     await preparing_violations_paths_on_pc(message)

    await select_start_category(message)
