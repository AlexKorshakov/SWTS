from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.core.bot.keyboards.replykeyboards.registration_finist_keybord import \
    registration_finish_keyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.reports.report_data_preparation import \
    set_violation_atr_data
from apps.core.bot.states import AnswerUserState
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


@MyBot.dp.message_handler(state=AnswerUserState.location, content_types=['location'])
async def location_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния location
    """
    chat_id = message.chat.id

    await set_violation_atr_data("coordinates", f'{message.location.latitude} \n{message.location.longitude}')

    logger.info(f'coordinates: {message.location.latitude} \n{message.location.longitude}')

    await set_violation_atr_data("latitude", message.location.latitude)
    await set_violation_atr_data("longitude", message.location.longitude)

    if violation_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await bot_send_message(chat_id=chat_id, text=Messages.Registration.confirm, reply_markup=keyboard)
