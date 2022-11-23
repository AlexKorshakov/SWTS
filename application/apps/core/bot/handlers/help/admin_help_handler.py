from aiogram import types
from aiogram.dispatcher.filters import Command

from app import MyBot
from config.config import ADMIN_ID
from apps.core.utils.misc import rate_limit
from apps.core.utils.secondary_functions.check_user_registration import check_user_access


@rate_limit(limit=5)
@MyBot.dp.message_handler(Command('admin_help'))
async def bot_help_buy(message: types.Message):
    """
    """
    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    if str(message.from_user.id) in ADMIN_ID:
        await message.answer(f"Команды для админа" '\n'
                             "Добавить / зарегестрировать пользователя /add_user" '\n')
