from loader import logger

logger.debug(f"{__name__} finish import")

from aiogram import types
from apps.MyBot import MyBot
from apps.core.bot.callbacks.callback_action import cb_start

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(cb_start.filter(action=["abort_registration"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery):
    """Действия при отмене регистрации
    """
    logger.info(f'User @{call.message.from_user.username}:{call.message.from_user.id} регистрация отменена')

