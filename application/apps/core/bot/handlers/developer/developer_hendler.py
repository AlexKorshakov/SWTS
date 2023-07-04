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
@MyBot.dp.message_handler(Command('developer'))
async def send_msg_from_developer(message: types.Message):
    """Отправка сообщения разработчику

    :param message:
    :return:
    """
    chat_id = message.chat.id
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} send message from developer')

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
