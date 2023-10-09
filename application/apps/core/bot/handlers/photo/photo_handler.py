from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.MyBot import MyBot

from apps.core.utils.misc import rate_limit
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.handlers.photo.qr_photo_processing import qr_code_processing
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.callbacks.select_start_category import select_start_category
from apps.core.bot.reports.report_data_preparation import preparing_violation_data, download_photo
from aiogram.dispatcher import FSMContext

logger.debug(f"{__name__} finish import")

logger.debug("message_handler 'photo'")


@rate_limit(limit=5)
@MyBot.dp.message_handler(content_types=["photo"])
async def photo_handler(message: types.Message, state: FSMContext, chat_id: str = None):
    """Обработчик сообщений с фото
    """

    hse_user_id = chat_id if chat_id else message.chat.id

    if not await check_user_access(chat_id=hse_user_id):
        return

    # val = await board_config(state, "start_violation_mes_id", 2).set_data()

    logger.info("photo_handler get photo")
    if await qr_code_processing(message, state=state):
        return

    start_photo_message_id = await board_config(state).set_data("start_violation_mes_id", message.message_id)
    logger.info(f"start_photo_message_id message.from_user.id {start_photo_message_id}")

    await preparing_violation_data(message=message, state=state, chat_id=hse_user_id)

    await download_photo(message, hse_user_id)

    await select_start_category(message)
