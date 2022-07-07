from aiogram import types
from aiogram.dispatcher.filters import Command

from app import MyBot
from loader import logger

from config.config import DEVELOPER_ID
from apps.core.bot.utils.misc import rate_limit


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('developer'))
async def send_msg_from_developer(message: types.Message):
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} send message from developer')

    text = f"Для связи с разработчиком начните сообщение с @dev и подробно опишите проблему," \
           f" пожелание и другую информацию"

    await message.answer(text)


@MyBot.dp.message_handler(content_types=['text'])
async def text_message_handler(message: types.Message):
    if "@dev" in message.text.strip().lower():

        logger.info(f'message from developer user {message.from_user.id} name {message.from_user.full_name}')

        text = f"Message from user {message.from_user.id} name {message.chat.full_name} \n" \
               f"https://t.me/{message.from_user.mention.replace('@', '')} \n" \
               f"message: {message.text.replace('@dev','')}"
        await MyBot.bot.send_message(chat_id=DEVELOPER_ID, text=text)
