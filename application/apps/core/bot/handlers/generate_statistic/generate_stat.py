import typing
from datetime import datetime, timedelta
from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Command

from apps.MyBot import MyBot
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import db_get_username, db_get_period_for_current_week
from apps.core.utils.generate_report.generate_stat.create_and_send_stat import create_and_send_stat
from apps.core.utils.misc import rate_limit
from apps.core.utils.secondary_functions.get_part_date import get_week_message, get_year_message
from loader import logger


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('generate_stat'))
async def stat_generate_handler(message: types.Message) -> None:
    """Формирование и отправка отчета пользователю
    :param message:
    :return: None
    """
    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    reply_markup = await add_period_inline_keyboard_with_action()
    await message.answer(text=Messages.Choose.period, reply_markup=reply_markup)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_today']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_today':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await call.message.answer(f'{Messages.Report.start_act} \n'
                                  f'{Messages.wait}')

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_act_date_period=None):
            logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_today_and_previous']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_today_and_previous':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await call.message.answer(f'{Messages.Report.start_report} \n'
                                  f'{Messages.wait}')

        now = datetime.now()
        previous = now - timedelta(days=1)
        act_date_period: list = [previous.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
        pprint(f'{act_date_period = }')

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_act_date_period=act_date_period):
            logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_week']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_current_week':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await call.message.answer(f'{Messages.Report.start_act} \n'
                                  f'{Messages.wait}')

        now = datetime.now()
        current_week: str = await get_week_message(current_date=now)
        current_year: str = await get_year_message(current_date=now)

        act_date_period = await db_get_period_for_current_week(current_week, current_year)
        pprint(f"{act_date_period = }")

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_act_date_period=act_date_period):
            logger.info(Messages.Report.generated_successfully)


async def add_period_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('за сегодня',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_today')))
    markup.add(types.InlineKeyboardButton('за сегодня и вчера',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_today_and_previous')))
    markup.add(types.InlineKeyboardButton('за текущую неделю',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_current_week')))
    return markup
