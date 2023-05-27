from loader import logger

logger.debug(f"{__name__} start import")
import asyncio
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Command
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import (db_get_period_for_current_week, db_get_username)
from apps.core.utils.generate_report.generate_act_prescription.create_and_send_act_prescription import \
    create_and_send_act_prescription
from apps.core.utils.misc import rate_limit
from apps.core.utils.secondary_functions.get_part_date import (
    get_week_message, get_year_message)
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('generate_act'))
async def act_generate_handler(message: types.Message) -> None:
    """Запуск генерации акта - предписания

    :param message:
    :return:
    """

    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    reply_markup = await add_period_inline_keyboard_with_action()
    await message.answer(text=Messages.Choose.period, reply_markup=reply_markup)


async def add_period_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('за сегодня',
                                          callback_data=posts_cb.new(id='-', action='gen_act_today')))
    markup.add(types.InlineKeyboardButton('за сегодня и вчера',
                                          callback_data=posts_cb.new(id='-', action='gen_act_today_and_previous')))
    markup.add(types.InlineKeyboardButton('за текущую неделю',
                                          callback_data=posts_cb.new(id='-', action='gen_act_current_week')))
    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_act_today']))
async def call_gen_act_today(call: types.CallbackQuery, callback_data: dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST

    :return:
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_act_today':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate act prescription')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate act prescription')

        await call.message.answer(f'{Messages.Report.start_act} \n'
                                  f'{Messages.wait}')

        now = datetime.now()
        act_date_period: list = [now.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
        logger.info(f"{chat_id = } {act_date_period = }")

        logger.info(f'User @{username}:{chat_id} generate act prescription')
        if await create_and_send_act_prescription(chat_id=chat_id, query_act_date_period=act_date_period):
            logger.info(Messages.Report.acts_generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_act_today_and_previous']))
async def call_gen_act_today_and_previous(call: types.CallbackQuery, callback_data: dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST

    :return:
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_act_today_and_previous':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate act prescription')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate act prescription')

        await call.message.answer(f'{Messages.Report.start_act} \n'
                                  f'{Messages.wait}')

        now = datetime.now()
        previous = now - timedelta(days=1)
        act_date_period: list = [previous.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
        logger.info(f"{chat_id = } {act_date_period = }")

        logger.info(f'User @{username}:{chat_id} generate act prescription')
        if await create_and_send_act_prescription(chat_id=chat_id, query_act_date_period=act_date_period):
            logger.info(Messages.Report.acts_generated_successfully)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['gen_act_current_week']))
async def call_gen_act_current_week(call: types.CallbackQuery, callback_data: dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST

    :return:
    """
    chat_id: int = call.message.chat.id
    username: str = await db_get_username(user_id=chat_id)
    action: str = callback_data['action']

    if action == 'gen_act_current_week':
        logger.info(f'User: @{username} user_id: {chat_id} choose {action} for generate act prescription')
        print(f'User: @{username} user_id: {chat_id} choose {action} for generate act prescription')

        await call.message.answer(f'{Messages.Report.start_act} \n'
                                  f'{Messages.wait}')

        now = datetime.now()
        current_week: str = await get_week_message(current_date=now)
        current_year: str = await get_year_message(current_date=now)

        act_date_period = await db_get_period_for_current_week(current_week, current_year)
        logger.info(f"{chat_id = } {act_date_period = }")

        logger.info(f'User @{username}:{chat_id} generate act prescription')
        if await create_and_send_act_prescription(chat_id=chat_id, query_act_date_period=act_date_period):
            logger.info(Messages.Report.acts_generated_successfully)


async def test():
    chat_id = 579531613
    now = datetime.now()
    # previous = now - timedelta(days=1)
    # act_date_period: list = [previous.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
    # logger.info(f"{chat_id = } {act_date_period = }")

    act_date_period: list = [now.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]
    logger.info(f"{chat_id = } {act_date_period = }")

    if await create_and_send_act_prescription(chat_id=chat_id, query_act_date_period=act_date_period):
        logger.info(Messages.Report.acts_generated_successfully)


if __name__ == "__main__":
    asyncio.run(test())
