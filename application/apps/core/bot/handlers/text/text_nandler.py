import traceback

from aiogram.dispatcher import FSMContext

from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.messages.messages import Messages
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


@MyBot.dp.message_handler(content_types=['text'], state='*')
async def text_message_handler(message: types.Message, state: FSMContext = None):
    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    # current_state = await state.get_state()
    # await state.finish()
    # logger.info(f'{await fanc_name()} state is finish {current_state = }')

    get_message_bot = message.text.strip().lower()
    logger.info(f'get_message_bot {get_message_bot}')
    await bot_send_message(chat_id=chat_id, text=f'Это текст \n {get_message_bot} \n {Messages.help_message}')


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])
