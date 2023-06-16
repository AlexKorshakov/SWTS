from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from apps.MyBot import MyBot, bot_send_message

from apps.core.utils.data_recording_processor.set_user_violation_data import \
    pre_set_violation_data

logger.debug(f"{__name__} finish import")


@MyBot.dp.message_handler(Text(equals='завершить регистрацию', ignore_case=True), state='*')
async def registration_finish_handler(message: types.Message, state: FSMContext, user_id: str = None):
    """Обработчик сообщений содержащих 'завершить регистрацию'

    """
    hse_user_id = message.chat.id if message else user_id

    await bot_send_message(chat_id=hse_user_id,
                           text="Запущена процедура регистрации данных. "
                                "Дождитесь сообщения об окончании.")
    await state.finish()

    await pre_set_violation_data(message)

    await bot_send_message(chat_id=hse_user_id, text="Данные зарегистрированы")
