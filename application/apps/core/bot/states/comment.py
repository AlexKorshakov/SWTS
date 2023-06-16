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


@MyBot.dp.message_handler(state=AnswerUserState.comment)
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """
    chat_id = message.chat.id

    await set_violation_atr_data("comment", message.text)

    await AnswerUserState.next()
    await bot_send_message(chat_id=chat_id, text="При необходимости отправьте своё местоположение")

    if violation_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await bot_send_message(chat_id=chat_id, text=Messages.Registration.confirm, reply_markup=keyboard)
