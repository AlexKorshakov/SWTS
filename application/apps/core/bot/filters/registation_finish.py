from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app import MyBot
from apps.core.bot.utils.set_user_violation_data import pre_set_violation_data


@MyBot.dp.message_handler(Text(equals='завершить регистрацию', ignore_case=True), state='*')
async def registration_finish_handler(message: types.Message, state: FSMContext):
    """Обработчик сообщений содержащих 'завершить регистрацию'
    """
    await MyBot.bot.send_message(message.chat.id, "данные зарегистрированы")
    await message.reply('ОК')
    await state.finish()

    await pre_set_violation_data(message)

