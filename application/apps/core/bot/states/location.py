from aiogram import types
from aiogram.dispatcher import FSMContext

from app import MyBot
from loader import logger

from apps.core.bot.data.report_data import violation_data
from apps.core.bot.keyboards.replykeyboards.registration_finist_keybord import registration_finish_keyboard
from apps.core.bot.states import AnswerUserState
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages


@MyBot.dp.message_handler(state=AnswerUserState.location, content_types=['location'])
async def process_comment(message: types.Message, state: FSMContext):
    """Обработчик состояния comment
    """
    violation_data["coordinates"] = f'{message.location.latitude} \n{message.location.longitude}'
    logger.info(f'coordinates: {violation_data["coordinates"]}')

    violation_data["latitude"] = message.location.latitude
    violation_data["longitude"] = message.location.longitude

    await write_json_file(data=violation_data, name=violation_data["json_full_name"])

    if violation_data.get("comment"):
        keyboard = await registration_finish_keyboard()
        await message.answer(text=Messages.Registration.confirm,
                             reply_markup=keyboard)
