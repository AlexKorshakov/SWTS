from aiogram import types
from aiogram.dispatcher import FSMContext

from app import MyBot
from apps.core.bot.keyboards.replykeyboards.registration_finist_keybord import registration_finish_keyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.core.bot.states import AnswerUserState


@MyBot.dp.message_handler(state=AnswerUserState.comment)
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """

    await set_violation_atr_data("comment", message.text)

    await AnswerUserState.next()
    await message.answer("При необходимости отправьте своё местположение")

    if violation_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await message.answer(text=Messages.Registration.confirm, reply_markup=keyboard)

