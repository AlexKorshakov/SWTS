from __future__ import annotations

import traceback

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from pandas import DataFrame
from datetime import datetime, timedelta, date
from pprint import pprint

from loader import logger
from apps.MyBot import MyBot, bot_send_message
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.messages.messages_test import Messages, msg
from apps.core.bot.bot_utils.bot_admin_notify import admin_notify
from apps.core.bot.bot_utils.check_user_registration import (check_user_access,
                                                             get_user_data_dict)
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.utils.misc import rate_limit
from apps.core.database.query_constructor import QueryConstructor
from apps.core.database.db_utils import (db_get_period_for_current_month,
                                         db_get_period_for_current_week,
                                         db_get_username,
                                         db_get_data_list,
                                         db_get_table_headers)
from apps.core.bot.handlers.generate.generate_stat_and_send import create_and_send_stat

logger.debug(f"{__name__} finish import")


@rate_limit(limit=10)
@MyBot.dp.callback_query_handler(posts_cb.filter(action=['generate_stat']))
@MyBot.dp.message_handler(Command('generate_stat'))
async def stat_generate_handler(message: types.Message, state: FSMContext = None, user_id: str = None) -> None:
    """Формирование и отправка отчета пользователю
    :param user_id:
    :param state:
    :param message:
    :return: None
    """
    try:
        hse_user_id = message.chat.id

    except AttributeError as err:
        hse_user_id = message.message.chat.id if message else user_id

    if not await check_user_access(chat_id=hse_user_id):
        return

    main_reply_markup = types.InlineKeyboardMarkup()
    hse_role_df: DataFrame = await get_role_receive_df()

    if not await check_user_access(chat_id=hse_user_id, role_df=hse_role_df):
        logger.error(f'access fail {hse_user_id = }')
        return

    main_reply_markup = await add_period_inline_keyboard_with_action(main_reply_markup)

    if await check_admin_access(chat_id=hse_user_id, role_df=hse_role_df):
        main_reply_markup = await add_inline_keyboard_with_action_for_admin(main_reply_markup)

    if await check_super_user_access(chat_id=hse_user_id, role_df=hse_role_df):
        main_reply_markup = await add_inline_keyboard_with_action_for_super_user(main_reply_markup)

    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.period, reply_markup=main_reply_markup)


async def add_period_inline_keyboard_with_action(markup: types.InlineKeyboardMarkup):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """
    markup.add(types.InlineKeyboardButton(
        text='за сегодня',
        callback_data=posts_cb.new(id='-', action='gen_stat_today'))
    )
    markup.add(types.InlineKeyboardButton(
        text='за сегодня и вчера',
        callback_data=posts_cb.new(id='-', action='gen_stat_today_and_previous'))
    )
    markup.add(types.InlineKeyboardButton(
        text='за текущую неделю',
        callback_data=posts_cb.new(id='-', action='gen_stat_current_week'))
    )
    markup.add(types.InlineKeyboardButton(
        text='за текущую месяц',
        callback_data=posts_cb.new(id='-', action='gen_stat_current_month'))
    )

    return markup


async def add_inline_keyboard_with_action_for_admin(markup: types.InlineKeyboardMarkup):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """
    markup.add(types.InlineKeyboardButton(
        text='АДМИН за текущую КН',
        callback_data=posts_cb.new(id='-', action='gen_stat_current_week_all'))
    )
    markup.add(types.InlineKeyboardButton(
        text='АДМИН за текущую мес',
        callback_data=posts_cb.new(id='-', action='gen_stat_current_month_all'))
    )
    markup.add(types.InlineKeyboardButton(
        text='АДМИН за все время',
        callback_data=posts_cb.new(id='-', action='gen_stat_all'))
    )
    return markup


async def add_inline_keyboard_with_action_for_super_user(markup: types.InlineKeyboardMarkup):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """
    # markup.add(types.InlineKeyboardButton(
    #     text='SU за текущую КН',
    #     callback_data=posts_cb.new(id='-', action='gen_stat_current_week_all'))
    # )
    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_today']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_today':
        return

    await notify_user_for_choice(call, data_answer=call.data)

    logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
    print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

    await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

    now = datetime.now()
    stat_date_period: list = [now.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]

    logger.info(f'User @{username}:{chat_id} generate stat')

    hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
    is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
    location: int = hse_user_data_dict.get('hse_location', None)

    kwargs = {
        'is_admin': is_admin,
        'location': location
    }

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_today_and_previous']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_today_and_previous':
        return
    logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
    print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

    await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_report} \n {Messages.wait}')

    now = datetime.now()
    previous = now - timedelta(days=1)
    stat_date_period: list = [previous.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]

    hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
    is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
    location: int = hse_user_data_dict.get('hse_location', None)

    kwargs = {
        'is_admin': is_admin,
        'location': location
    }

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_week']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_current_week':
        return

    logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')
    print(f'User: @{username} user_id: {chat_id} choose {action} for generate stat')

    await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.start_act} \n {Messages.wait}')

    now = datetime.now()
    current_week: str = await get_week_message(current_date=now)
    current_year: str = await get_year_message(current_date=now)

    stat_date_period = await db_get_period_for_current_week(current_week, current_year)

    hse_user_data_dict, hse_user_role_dict = await get_user_data_dict(chat_id)
    is_admin: int = hse_user_role_dict.get('hse_role_is_admin', None)
    location: int = hse_user_data_dict.get('hse_location', None)

    kwargs = {
        'is_admin': is_admin,
        'location': location
    }

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_month']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_current_month':
        return

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

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_week_all']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_current_week_all':
        return

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

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_current_month_all']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_current_month_all':
        return

    await notify_user_for_choice(call, data_answer=call.data)

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

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_stat_all']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action != 'gen_stat_all':
        return

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

    await board_config(state, "stat_date_period", stat_date_period).set_data()
    if await create_and_send_stat(chat_id=chat_id, query_period=stat_date_period, **kwargs):
        logger.info(Messages.Report.generated_successfully)


async def check_admin_access(chat_id: int | str, role_df: DataFrame = None):
    """

    :param role_df:
    :param chat_id:
    :return:
    """
    admin_id_list: list = await get_id_list(
        hse_user_id=chat_id, user_role='hse_role_is_admin', hse_role_df=role_df
    )
    if not admin_id_list:
        logger.error(f'{await fanc_name()} access fail {chat_id = }')
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    if chat_id not in admin_id_list:
        logger.error(f'{await fanc_name()} access fail {chat_id = }')
        return False

    logger.info(f"user_access_granted for {chat_id = }")
    await user_access_granted(chat_id, role=await fanc_name(), notify=True)
    return True


async def check_super_user_access(chat_id: int | str, role_df: DataFrame = None):
    """

    :param role_df:
    :param chat_id:
    :return:
    """
    super_user_id_list: list = await get_id_list(
        hse_user_id=chat_id, user_role='hse_role_is_super_user', hse_role_df=role_df
    )
    if not super_user_id_list:
        logger.warning(f'{await fanc_name()} access fail {chat_id = }')
        await user_access_fail(chat_id, hse_id=chat_id)
        return False

    if chat_id not in super_user_id_list:
        logger.warning(f'{await fanc_name()} access fail {chat_id = }')
        return False

    logger.info(f"user_access_granted for {chat_id = }")
    await user_access_granted(chat_id, role=await fanc_name())
    return True


async def get_role_receive_df() -> DataFrame | None:
    """Получение df с ролями пользователя

    :return:
    """

    db_table_name: str = 'core_hseuser'
    kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
    }
    query: str = await QueryConstructor(table_name=db_table_name, **kwargs).prepare_data()
    datas_query: list = await db_get_data_list(query=query)
    if not datas_query:
        return None

    if not isinstance(datas_query, list):
        return None

    clean_headers: list = [item[1] for item in await db_get_table_headers(table_name=db_table_name)]
    if not clean_headers:
        return None

    try:
        hse_role_receive_df: DataFrame = DataFrame(datas_query, columns=clean_headers)

    except Exception as err:
        logger.error(f"create_dataframe {repr(err)}")
        return None

    return hse_role_receive_df


async def get_id_list(hse_user_id: str | int, user_role: str = None, hse_role_df: DataFrame = None) -> list:
    """Получение id"""

    if not await check_dataframe_role(hse_role_df, hse_user_id):
        hse_role_df: DataFrame = await get_role_receive_df()
        if not await check_dataframe_role(hse_role_df, hse_user_id):
            return []

    try:
        current_act_violations_df: DataFrame = hse_role_df.loc[
            hse_role_df[user_role] == 1]

    except Exception as err:
        logger.error(f"loc dataframe {repr(err)}")
        return []

    unique_hse_telegram_id: list = current_act_violations_df.hse_telegram_id.unique().tolist()
    if not unique_hse_telegram_id:
        return []

    return unique_hse_telegram_id


async def check_dataframe_role(dataframe: DataFrame, hse_user_id: str | int) -> bool:
    """Проверка dataframe на наличие данных

    :param dataframe:
    :param hse_user_id: id пользователя
    :return:
    """
    if dataframe is None:
        # text_violations: str = 'не удалось получить данные!'
        # logger.error(f'{hse_user_id = } {text_violations}')
        return False

    if dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}')
        return False

    return True


async def user_access_granted(chat_id: int, role: str = None, notify=False):
    """Отправка сообщения - доступ разрешен"""

    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text=f'{chat_id}', url=f"tg://user?id={chat_id}"))

    notify_text: str = f'доступ разрешен {chat_id = } {role = }'
    logger.debug(notify_text)
    if notify:
        await admin_notify(user_id=chat_id, notify_text=notify_text)


async def user_access_fail(chat_id: int, notify_text: str = None, hse_id: str = None):
    """Отправка сообщения о недостатке прав
    """
    hse_id = hse_id if hse_id else chat_id

    try:
        default_answer_text: str = 'У вас нет прав доступа \n По всем вопросам обращайтесь к администратору\n' \
                                   'https://t.me/AlexKor_MSK \n\n'

        part_1 = f"{await msg(hse_id, cat='error', msge='access_fail', default=default_answer_text).g_mas()}"
        part_2 = f"{await msg(hse_id, cat='help', msge='help_message', default=Messages.help_message).g_mas()}"
        answer_text = f'{part_1}\n\n{part_2}'
        print(f'{answer_text = }')

        await bot_send_message(chat_id=chat_id, text=answer_text, disable_web_page_preview=True)
        return

    except Exception as err:
        logger.error(f'User {chat_id} ошибка уведомления пользователя {repr(err)}')
        await admin_notify(user_id=chat_id, notify_text=notify_text)

    finally:
        if not notify_text:
            notify_text: str = f'User {chat_id} попытка доступа к функциям без регистрации'

        button = types.InlineKeyboardButton('user_actions',
                                            callback_data=posts_cb.new(id='-', action='admin_user_actions'))
        await admin_notify(
            user_id=chat_id,
            notify_text=notify_text,
            button=button
        )


async def str_to_datetime(date_str: str) -> date:
    """Преобразование str даты в datetime

    :param
    """

    current_date = None
    try:
        if isinstance(date_str, str):
            current_date: date = datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError as err:
        logger.error(f"{repr(err)}")

    return current_date


async def get_day_message(current_date: datetime | str = None) -> str:
    """Обработчик сообщений с фото
    Получение номер str дня из сообщения в формате dd
    """

    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()
    return str("0" + str(current_date.day) if current_date.day < 10 else str(current_date.day))


async def get_week_message(current_date: datetime | str = None) -> str:
    """Обработчик сообщений с фото
    Получение номер str недели из сообщения в формате dd
    """
    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()
    week = current_date.isocalendar()[1]
    return str("0" + str(week) if week < 10 else str(week))


async def get_month_message(current_date: datetime | str = None) -> str:
    """Получение номер str месяца из сообщения в формате mm
    """
    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()
    return str("0" + str(current_date.month) if int(current_date.month) < 10 else str(current_date.month))


async def get_year_message(current_date: datetime | str = None) -> str:
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()

    return str(current_date.year)


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


async def notify_user_for_choice(call_msg: types.CallbackQuery | types.Message, user_id: int | str = None,
                                 data_answer: str = None) -> bool:
    """Уведомление пользователя о выборе + логирование

    :param data_answer:
    :param user_id: int | str id пользователя
    :param call_msg:
    :return None :
    """

    if isinstance(call_msg, types.CallbackQuery):

        for i in ('previous_paragraph', 'move_up', 'move_down'):
            if i in call_msg.data: return True

        mesg_text: str = f"Выбрано: {data_answer}"
        if call_msg.data in call_msg.message.text:
            mesg_list: list = [item for item in call_msg.message.text.split('\n\n') if call_msg.data in item]
            mesg_text = f"Выбрано: {mesg_list[0]}"

        try:
            hse_user_id = call_msg.message.chat.id if call_msg else user_id
            logger.debug(f"{hse_user_id = } Выбрано: {data_answer} {call_msg.data}")
            await call_msg.message.edit_text(text=mesg_text, reply_markup=None)
            return True

        except Exception as err:
            logger.debug(f"{call_msg.message.chat.id = } {repr(err)}")

    if isinstance(call_msg, types.Message):

        for i in ('previous_paragraph', 'move_up', 'move_down'):
            if i in call_msg.text: return True

        mesg_text: str = f"Выбрано: {data_answer}"
        if call_msg.text in call_msg.text:
            mesg_list: list = [item for item in call_msg.text.split('\n\n') if call_msg.text in item]
            mesg_text = f"Выбрано: {mesg_list[0] if mesg_list else ''}"

        try:
            hse_user_id = call_msg.chat.id if call_msg else user_id
            logger.debug(f"{hse_user_id = } Выбрано: {data_answer} {call_msg.text}")
            await call_msg.edit_text(text=mesg_text, reply_markup=None)
            return True

        except Exception as err:
            logger.debug(f"{call_msg.chat.id = } {repr(err)}")
