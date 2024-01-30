from __future__ import annotations

from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.MyBot import bot_send_message, MyBot
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.bot.messages.messages_test import msg
from apps.core.checker.periodic_check_unclosed_points import check_acts_prescriptions_status
from loader import logger


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['check_acts_prescriptions_status']))
async def check_acts_prescriptions_status_answer(call: types.CallbackQuery, callback_data: dict[str, str],
                                                 state: FSMContext = None):
    """

    :return: None
    """
    hse_user_id = call.message.chat.id
    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    msg_text = await msg(hse_user_id, cat='error', msge='error_action', default=Messages.Error.error_action).g_mas()
    await bot_send_message(chat_id=hse_user_id, text=msg_text)
    await check_acts_prescriptions_status()
