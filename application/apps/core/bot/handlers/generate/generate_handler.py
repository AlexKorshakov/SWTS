from loader import logger
logger.debug(f"{__name__} start import")

import typing
from aiogram import types
from aiogram.dispatcher.filters import Command

from apps.MyBot import MyBot
from apps.core.bot.handlers.generate_act.generate_act import act_generate_handler
from apps.core.bot.handlers.generate_report.generate_daily_report import report_generate_handler
from apps.core.bot.handlers.generate_statistic.generate_stat import stat_generate_handler
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.utils.misc import rate_limit

logger.debug(f"{__name__} finish import")


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('generate'))
async def generate_handler(message: types.Message):
    """Обработка команд генерации документов

    :return:
    """

    chat_id = message.chat.id

    if not await check_user_access(chat_id=chat_id):
        logger.error(f'access fail {chat_id = }')
        return

    reply_markup = await add_doc_inline_keyboard_with_action()

    await message.answer(text=Messages.Choose.generate_doc, reply_markup=reply_markup)


async def add_doc_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Акт-предписание',
                                          callback_data=posts_cb.new(id='-', action='generate_act')))
    markup.add(types.InlineKeyboardButton('Общий отчет',
                                          callback_data=posts_cb.new(id='-', action='generate_report')))
    markup.add(types.InlineKeyboardButton('Статистика',
                                          callback_data=posts_cb.new(id='-', action='generate_stat')))
    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['generate_act']))
async def call_generate_act(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """

    await act_generate_handler(call.message)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['generate_report']))
async def call_generate_report(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """

    await report_generate_handler(call.message)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['generate_stat']))
async def call_generate_stat(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """

    await stat_generate_handler(call.message)
