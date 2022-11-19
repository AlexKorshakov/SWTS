from aiogram import types
from loader import logger

from apps.core.bot.keyboards.inline.select_category import bild_inline_keyboard


async def big_category(call: types.CallbackQuery, big_menu_list, num_col=2):
    """Создание больших inline клавиатур с заданными параметрами
    @param call: обьект обратного вызова
    @param big_menu_list: list  с названиями кнопок
    @param num_col: колличество колонок в клавиатуре
    @return:
    """
    i_start = 0
    num = int(len(big_menu_list))
    while i_start < num:
        i_stop = i_start + 10
        try:
            await bild_inline_keyboard(call.message, some_list=big_menu_list[i_start:i_stop], num_col=num_col)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
            await bild_inline_keyboard(call.message, some_list=big_menu_list[i_start:num], num_col=num_col)

        i_start += 10
