from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import (global_reg_form, headlines_data,
                                               user_data, violation_data)
from apps.core.utils.misc import rate_limit
from apps.MyBot import MyBot
from config.config import ADMIN_ID

logger.debug(f"{__name__} finish import")


class NamedDict(dict):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs.pop('name')
        except KeyError:
            raise KeyError('a "name" keyword argument must be supplied')
        super(NamedDict, self).__init__(*args, **kwargs)

    @classmethod
    def fromkeys(cls, name, seq, value=None):
        return cls(dict.fromkeys(seq, value), name=name)

    @property
    def name(self):
        return self._name


@rate_limit(limit=5)
@MyBot.dp.message_handler(Command('cancel'), state='*')
@MyBot.dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    """Корректирование уже введённых значений на локальном pc и на google drive
    :return:
    """

    chat_id = call.from_user.id
    if not await check_user_access(chat_id=chat_id):
        return

    dict_list = [NamedDict.fromkeys('violation_data', violation_data),
                 NamedDict.fromkeys('user_data', user_data),
                 NamedDict.fromkeys('global_reg_form', global_reg_form),
                 NamedDict.fromkeys('headlines_data', headlines_data)]

    for items_data in dict_list:
        items_data_name = [item for item in items_data.keys()]
        logger.debug(f"Report {str(items_data.name)} {items_data}")
        if items_data_name:
            items_data.clear()
            logger.info(f"Report is clear {str(items_data.name)} {items_data}")

    board_config.menu_level = 1
    board_config.menu_list = []

    board_config.violation_menu_list = []
    board_config.violation_file = []
    board_config.previous_level = ''

    board_config.current_file = None

    await call.answer(text=Messages.all_canceled)
    await MyBot.bot.send_message(chat_id=ADMIN_ID, text=f'cancel_all from {chat_id}')
    # await call.answer(text='Cancelled.')

    current_state = await state.get_state()
    logger.info(f'Cancelling state {current_state}')
    await state.finish()
    if current_state is None:
        logger.info(f'Cancelling state {current_state}')
        return

    await state.finish()
