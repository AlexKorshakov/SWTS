import traceback

from aiogram.dispatcher import FSMContext

from apps.core.bot.messages.messages import Messages
from apps.core.bot.messages.messages_test import msg
from apps.core.settyngs import get_sett
from loader import logger

logger.debug(f"{__name__} start import")

from aiogram import types
from aiogram.dispatcher.filters import Command
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.utils.misc import rate_limit
from apps.MyBot import MyBot, bot_send_message
from config.config import DEVELOPER_ID

logger.debug(f"{__name__} finish import")


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('developer'), state='*')
async def send_msg_from_developer(message: types.Message, state: FSMContext = None):
    """Отправка сообщения разработчику

    :param state:
    :param message:
    :return:
    """
    chat_id = message.chat.id
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} send message from developer')

    current_state = await state.get_state()
    await state.finish()
    logger.info(f'{await fanc_name()} state is finish {current_state = }')

    if not get_sett(cat='enable_features', param='use_msg_from_developer').get_set():
        msg_text: str = f"{await msg(chat_id, cat='error', msge='features_disabled', default=Messages.Error.features_disabled).g_mas()}"
        await bot_send_message(chat_id=chat_id, text=msg_text, disable_web_page_preview=True)
        return

    answer_text: str = "Для связи с разработчиком напишите https://t.me/AlexKor_MSK"
    await bot_send_message(chat_id=chat_id, text=answer_text)


@MyBot.dp.message_handler(content_types=['text'])
async def text_message_handler(message: types.Message):
    """

    :param message:
    :return:
    """

    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    if "@dev" in message.text.strip().lower():
        logger.info(f'message from developer user {message.from_user.id} name {message.from_user.full_name}')

        text = f"Message from user {message.from_user.id} name {message.chat.full_name} \n" \
               f"https://t.me/{message.from_user.mention.replace('@', '')} \n" \
               f"message: {message.text.replace('@dev', '')}"
        await bot_send_message(chat_id=DEVELOPER_ID, text=text)


async def fanc_name() -> str:
    """Возвращает имя вызываемой функции"""
    stack = traceback.extract_stack()
    return str(stack[-2][2])
