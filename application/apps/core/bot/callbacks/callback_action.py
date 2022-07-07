from loader import logger

logger.debug("callback_action")

from aiogram.utils.callback_data import CallbackData

cb_start = CallbackData("fabnum", "action")
