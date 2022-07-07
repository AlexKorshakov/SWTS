from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from loader import logger


def setup_middlewares(dp: Dispatcher):
    logger.info("Установка middlewares...")
    dp.middleware.setup(ThrottlingMiddleware())
