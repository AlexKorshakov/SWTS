from aiogram import types
from aiogram.dispatcher import FSMContext

from app import MyBot
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.core.bot.states import AnswerUserState


# Сюда приходит ответ с description, state=состояние
@MyBot.dp.message_handler(state=AnswerUserState.description)
async def process_description(message: types.Message, state: FSMContext):
    """Обработчик состояния description
    """
    await set_violation_atr_data("description", message.text)

    await AnswerUserState.next()
    await message.answer(Messages.Enter.comment)

