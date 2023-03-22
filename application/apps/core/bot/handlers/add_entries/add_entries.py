from loader import logger

logger.debug(f"{__name__} start import")

import typing
from aiogram import types
from aiogram.dispatcher.filters import Command

from apps.MyBot import MyBot
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.utils.misc import rate_limit

logger.debug(f"{__name__} finish import")


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('add_entries'))
async def add_entries_handler(message: types.Message):
    """Обработка команд генерации документов

    :return:
    """

    chat_id = message.chat.id

    if not await check_user_access(chat_id=chat_id):
        logger.error(f'access fail {chat_id = }')
        return

    reply_markup = await add_entries_inline_keyboard_with_action()

    await message.answer(text=Messages.Choose.generate_doc, reply_markup=reply_markup)


async def add_entries_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Записи в базу',
                                          callback_data=posts_cb.new(id='-', action='add_entries')))

    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['add_entries']))
async def call_add_entries(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    pass
    # await act_generate_handler(call.message)