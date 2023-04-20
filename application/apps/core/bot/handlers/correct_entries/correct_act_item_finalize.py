from __future__ import annotations
import asyncio

from datetime import datetime

from aiogram import types
from pandas import DataFrame

from apps.MyBot import MyBot, bot_send_message
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.handlers.correct_entries.correct_entries_handler import correct_entries_handler
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages, LogMessage
from apps.core.database.db_utils import db_get_data_list, db_get_table_headers, db_update_column_value, \
    db_update_table_column_value
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_act_item_finalize']))
async def call_correct_act_item_finalize(call: types.CallbackQuery = None, callback_data: dict[str, str] = None,
                                         user_id: int | str = None):
    """Обработка ответов содержащихся в callback_data "Финализировать и записать"
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')
    logger.debug(f'{callback_data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    if not call:
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_call)
        return

    if not call.message.values['text']:
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_call_text)
        return

    item_number_text = call.message.values['text'].split('_')[-1]
    logger.debug(f'{hse_user_id = } {item_number_text = }')
    await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)


async def get_now() -> str:
    """Возвращает текущую дату и время.
    :return: str
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


async def test():
    await call_correct_act_item_finalize(user_id='373084462')


if __name__ == '__main__':
    asyncio.run(test())
