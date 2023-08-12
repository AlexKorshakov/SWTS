from apps.core.bot.messages.messages_test import msg
from apps.core.settyngs import get_sett
from loader import logger

logger.debug(f"{__name__} start import")

import typing
from aiogram import types
from aiogram.dispatcher.filters import Command

from apps.MyBot import MyBot, bot_send_message
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

    if not get_sett(cat='enable_features', param='use_catalog_func').get_set():
        msg_text: str = f"{await msg(chat_id, cat='error', msge='features_disabled', default=Messages.Error.features_disabled).g_mas()}"
        await bot_send_message(chat_id=chat_id, text=msg_text, disable_web_page_preview=True)
        return

    reply_markup = await add_entries_inline_keyboard_with_action()
    await bot_send_message(chat_id=chat_id, text=Messages.Choose.generate_doc, reply_markup=reply_markup)


async def add_entries_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавление нормативки',
                                          callback_data=posts_cb.new(id='-', action='add_entries_normative_doc')))

    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['add_entries_normative_doc']))
async def call_add_entries(call: types.CallbackQuery, callback_data: typing.Dict[str, str], user_id=None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST

    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = } {callback_data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    # TODO Delete
    logger.error(f'{hse_user_id = } Messages.Error.error_action')
    msg_text = await msg(hse_user_id, cat='error', msge='error_action', default=Messages.Error.error_action).g_mas()
    await bot_send_message(chat_id=hse_user_id, text=msg_text)
