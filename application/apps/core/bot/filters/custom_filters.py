from loader import logger

logger.debug(f"{__name__} start import")

from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType
from config.config import ADMIN_ID

logger.debug(f"{__name__} finish import")


def is_group(message: types.Message):
    return ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP])


def is_private(message: types.Message):
    return ChatTypeFilter(ChatType.PRIVATE)


def is_channel(message: types.Message):
    return ChatTypeFilter(ChatType.CHANNEL)


def is_sudo(message: types.Message):
    return message.from_user.id in ADMIN_ID
