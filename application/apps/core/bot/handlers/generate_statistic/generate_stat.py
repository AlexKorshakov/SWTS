from loader import logger

logger.debug(f"{__name__} start import")
import typing
from datetime import datetime, timedelta
from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Command
from apps.core.bot.bot_utils.check_user_registration import (
    check_user_access, get_user_data_dict)
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import (db_get_period_for_current_month,
                                         db_get_period_for_current_week,
                                         db_get_username)
from apps.core.utils.generate_report.generate_stat.create_and_send_stat import \
    create_and_send_stat
from apps.core.utils.misc import rate_limit
from apps.core.utils.secondary_functions.get_part_date import (
    get_month_message, get_week_message, get_year_message)
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


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

    _, hse_user_role_dict = await get_user_data_dict(chat_id)
    is_admin: bool = hse_user_role_dict.get('hse_role_is_admin', None)

    reply_markup = await stat_add_period_inline_keyboard_with_action(is_admin)

    await bot_send_message(chat_id=chat_id, text=Messages.Choose.period, reply_markup=reply_markup)


async def stat_add_period_inline_keyboard_with_action(is_admin: bool = None):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text='за сегодня',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_today')))
    markup.add(types.InlineKeyboardButton(text='за сегодня и вчера',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_today_and_previous')))
    markup.add(types.InlineKeyboardButton(text='за текущую неделю',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_current_week')))
    markup.add(types.InlineKeyboardButton(text='за текущую месяц',
                                          callback_data=posts_cb.new(id='-', action='gen_stat_current_month')))
    if is_admin:
        markup.add(types.InlineKeyboardButton(text='АДМИН за текущую КН',
                                              callback_data=posts_cb.new(id='-', action='gen_stat_current_week_all')))
        markup.add(types.InlineKeyboardButton(text='АДМИН за текущую мес',
                                              callback_data=posts_cb.new(id='-', action='gen_stat_current_month_all')))
        markup.add(types.InlineKeyboardButton(text='АДМИН за все время',
                                              callback_data=posts_cb.new(id='-', action='gen_stat_all')))

    return markup


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

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

        now = datetime.now()
        stat_date_period: list = [now.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
        pprint(f'{stat_date_period = }')

        logger.info(f'User @{username}:{chat_id} generate stat')

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
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

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_report} \n {Messages.wait}')

        now = datetime.now()
        previous = now - timedelta(days=1)
        stat_date_period: list = [previous.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
        pprint(f'{stat_date_period = }')

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
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

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

        now = datetime.now()
        current_week: str = await get_week_message(current_date=now)
        current_year: str = await get_year_message(current_date=now)

        stat_date_period = await db_get_period_for_current_week(current_week, current_year)
        pprint(f"{stat_date_period = }")

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
            logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_month']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_current_month':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

        now = datetime.now()
        current_month: str = await get_month_message(current_date=now)
        current_year: str = await get_year_message(current_date=now)

        stat_date_period = await db_get_period_for_current_month(
            current_month=current_month, current_year=current_year
        )
        pprint(f"{stat_date_period = }")

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
            logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_week_all']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_current_week_all':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

        now = datetime.now()
        current_week: str = await get_week_message(current_date=now)
        current_year: str = await get_year_message(current_date=now)

        stat_date_period = await db_get_period_for_current_week(current_week, current_year)
        pprint(f"{stat_date_period = }")

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
            logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_month_all']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_current_month_all':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

        now = datetime.now()
        current_month: str = await get_month_message(current_date=now)
        current_year: str = await get_year_message(current_date=now)

        stat_date_period = await db_get_period_for_current_month(
            current_month=current_month, current_year=current_year
        )
        logger.info(f"{stat_date_period = }")

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
            logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_all']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_stat_all':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')
        now = datetime.now()
        stat_date_period: list = ['01.01.2022', now.strftime("%d.%m.%Y"), ]
        logger.info(f"{stat_date_period = }")

        hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
        is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
        location: int = hse_user_data_dict.get('hse_location', None)

        kwargs = {
            'is_admin': is_admin,
            'location': location
        }

        logger.info(f'User @{username}:{chat_id} generate stat')
        if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
            logger.info(Messages.Report.generated_successfully)
