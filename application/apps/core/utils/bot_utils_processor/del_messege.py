import asyncio
from contextlib import suppress

from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from apps.core.bot.data import board_config
from config.config import BOT_DELETE_MESSAGE

from apps.MyBot import MyBot


async def bot_delete_message(chat_id: str, message_id: str, sleep_time: int = 1):
    """Удаление сообщений по таймеру

    :param message_id: id сообщения
    :param chat_id: id чата из которого удаляется сообщение
    :param sleep_time:int - время в секундах
    """
    if BOT_DELETE_MESSAGE:
        await asyncio.sleep(sleep_time)
        with suppress(MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound):
            await MyBot.bot.delete_message(chat_id=chat_id, message_id=message_id)


async def cyclical_deletion_message(chat_id: str):
    """Цикличное удаление сообщений

    :param chat_id: id чата из которого удаляется сообщение
    :return:
    """
    mes_id = board_config.start_violation_mes_id + 1

    while mes_id != board_config.stop_violation_mes_id + 3:
        await bot_delete_message(chat_id=chat_id, message_id=str(mes_id), sleep_time=5)
        mes_id += 1
