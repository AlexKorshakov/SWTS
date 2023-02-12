from loader import logger

logger.debug(f"{__name__} start import")

from aiogram.utils.callback_data import CallbackData

logger.debug(f"{__name__} finish import")

cb_start = CallbackData("fabnum", "action")
