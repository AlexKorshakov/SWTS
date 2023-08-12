from __future__ import annotations

from aiogram import types

from apps.MyBot import MyBot
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from loader import logger


@MyBot.dp.callback_query_handler(lambda call: 'level_3__' in call.data)
async def call_level_3_answer(call: types.CallbackQuery, user_id: int | str = None) -> None:
    """Обработка ответов
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = } {call.data = }')

    msg_id = call.message.message_id
    # await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return