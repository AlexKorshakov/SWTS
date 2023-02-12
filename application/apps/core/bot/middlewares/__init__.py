from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware

logger.debug(f"{__name__} finish import")


def setup_middlewares(dp: Dispatcher):
    logger.info("Установка middlewares...")
    dp.middleware.setup(ThrottlingMiddleware())
