from loader import logger

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from apps.MyBot import MyBot

logger.debug("start registation_finish")

from apps.core.utils.data_recording_processor.set_user_violation_data import pre_set_violation_data

logger.debug("stop registation_finish")


@MyBot.dp.message_handler(Text(equals='завершить регистрацию', ignore_case=True), state='*')
async def registration_finish_handler(message: types.Message, state: FSMContext):
    """Обработчик сообщений содержащих 'завершить регистрацию'

    """
    await MyBot.bot.send_message(message.chat.id,
                                 "Запущена процедура регистрации данных. "
                                 "Дождитесь сообщения об окончании.")
    await state.finish()

    await pre_set_violation_data(message)

    await MyBot.bot.send_message(message.chat.id, "Данные зарегистрированы")
