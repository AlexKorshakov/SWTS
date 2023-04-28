from __future__ import annotations
import asyncio
import traceback
import typing
from datetime import datetime

from aiogram import types
from pandas import DataFrame

from apps.MyBot import MyBot, bot_send_message, bot_delete_message
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.handlers.correct_entries.correct_support import create_user_dataframe
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb, build_inlinekeyboard
from apps.core.bot.messages.messages import Messages, LogMessage
from apps.core.database.db_utils import db_get_data_list, db_get_table_headers
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_acts']))
async def call_correct_acts(call: types.CallbackQuery = None, callback_data: typing.Dict[str, str] = None,
                            user_id: int | str = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """

    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    query_kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "finished_id": "!= 1",
            "status_id": "!= 1",
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    violations_dataframe: DataFrame = await create_lite_dataframe_from_query(query=query, table_name='core_violations')
    if violations_dataframe is None:
        text_violations: str = 'Незакрытых актов не обнаружено!'
        await bot_send_message(chat_id=hse_user_id, text=text_violations)
        return True

    if violations_dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}  \n{query = }')
        return False

    user_violations: DataFrame = await create_user_dataframe(hse_user_id, violations_dataframe)
    if user_violations is None:
        text_violations: str = 'Незакрытых актов не обнаружено!'
        await bot_send_message(chat_id=hse_user_id, text=text_violations)
        return True
    if user_violations.empty:
        return False

    text_violations: str = await text_processor_user_violations(user_violations)

    reply_markup: types.InlineKeyboardMarkup = await add_correct_inline_keyboard_with_action(user_violations)

    await bot_send_message(chat_id=hse_user_id, text=text_violations, reply_markup=reply_markup)

    # msg_id = call.message.message_id
    # await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)

    return True


@MyBot.dp.callback_query_handler(lambda call: 'act_number_' in call.data)
async def act_number_answer(call: types.CallbackQuery, user_id: str = None) -> None:
    """Обработка ответов
    """

    act_number = call.data

    hse_user_id = call.message.chat.id if call else user_id
    logger.info(f'{hse_user_id = } {call.data = }')

    text_violations = f'Выбрано {act_number}'

    reply_markup = await add_act_inline_keyboard_with_action()

    await bot_send_message(chat_id=hse_user_id, text=text_violations, reply_markup=reply_markup)


async def add_act_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Финализировать и записать',
                                          callback_data=posts_cb.new(id='-', action='correct_act_finalize')))
    markup.add(types.InlineKeyboardButton('Исправить отдельные пункты',
                                          callback_data=posts_cb.new(id='-', action='correct_act_item_correct')))
    markup.add(types.InlineKeyboardButton('Удалить номер из базы',
                                          callback_data=posts_cb.new(id='-', action='correct_act_delete_from_base')))
    markup.add(types.InlineKeyboardButton('Удалить акт и пункты',
                                          callback_data=posts_cb.new(id='-', action='correct_act_delete')))
    return markup


async def add_correct_inline_keyboard_with_action(user_violations: DataFrame):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    unique_acts_numbers: list = user_violations.act_number.unique().tolist()
    unique_acts_numbers: list = [f'act_number_{item}' for item in unique_acts_numbers if item]

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = unique_acts_numbers
    count_col = board_config.count_col = 2

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level)

    return reply_markup


async def get_hse_role_receive_notifications_list() -> list:
    """Получение списка пользователей кому отправляются уведомления
    """
    db_table_name: str = 'core_hseuser'
    query: str = f'SELECT * FROM {db_table_name}'
    datas_query: list = await db_get_data_list(query=query)

    if not datas_query:
        return []

    if not isinstance(datas_query, list):
        return []

    clean_headers: list = [item[1] for item in await db_get_table_headers(table_name=db_table_name)]
    if not clean_headers:
        return []

    try:
        hse_role_receive_df: DataFrame = DataFrame(datas_query, columns=clean_headers)
    except Exception as err:
        logger.error(f"create_dataframe {repr(err)}")
        return []

    current_act_violations_df: DataFrame = hse_role_receive_df.loc[
        hse_role_receive_df['hse_role_receive_notifications'] == 1
        ]

    unique_hse_telegram_id: list = current_act_violations_df.hse_telegram_id.unique().tolist()

    return unique_hse_telegram_id


async def text_processor_user_violations(user_violations: DataFrame) -> str:
    """Формирование текста для отправки пользователю"""

    unique_acts_numbers: list = user_violations.act_number.unique().tolist()

    act_description: list = []
    len_unique_acts: int = 0
    for act_number in unique_acts_numbers:

        if not act_number:
            continue

        query_kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "act_number": act_number,
            },
        }
        query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

        violations_dataframe: DataFrame = await create_lite_dataframe_from_query(
            query=query, table_name='core_violations')

        if violations_dataframe.empty:
            logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')

        len_act_violations: int = len(violations_dataframe) if not violations_dataframe.empty else 0

        act_violations_df = user_violations.copy(deep=True)
        current_act_violations: DataFrame = act_violations_df.loc[act_violations_df['act_number'] == act_number]

        unclosed_points_df = current_act_violations.loc[current_act_violations['status_id'] != 1]
        unclosed_points: int = len(unclosed_points_df)

        query_kwargs: dict = {
            "action": 'SELECT',
            "subject": '*',
            "conditions": {
                "act_number": act_number,
            },
        }
        query: str = await QueryConstructor(None, 'core_actsprescriptions', **query_kwargs).prepare_data()

        violations_dataframe: DataFrame = await create_lite_dataframe_from_query(query=query,
                                                                                 table_name='core_actsprescriptions')

        if violations_dataframe is None:
            logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')
            continue

        if violations_dataframe.empty:
            logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')
            continue

        act_date = violations_dataframe.act_date.unique().tolist()[0]

        item_info = f'Ном: {act_number} от {act_date} всего пунктов: {len_act_violations} Незакрыто: {unclosed_points}'
        act_description.append(item_info)
        len_unique_acts += 1

    non_acts_items_df: DataFrame = user_violations.loc[user_violations['act_number'] == '']
    non_acts_items: int = len(non_acts_items_df)
    non_acts_text: str = f'Записей вне актов всего: {non_acts_items}'

    header_text: str = f'У вас есть незакрытые акты: Всего актов {len_unique_acts}'

    acts_text: str = '\n'.join(act_description)

    final_text: str = f'{header_text} \n\n{acts_text} \n\n{non_acts_text}'
    return final_text


async def create_lite_dataframe_from_query(query: str, table_name: str) -> DataFrame or None:
    """Возвращает list с нарушениями

    :return: DataFrame or None
    """

    if not query:
        logger.error(f"{LogMessage.Check.no_query} ::: {await get_now()}")
        return None

    violations_data: list = await db_get_data_list(query=query)

    if not violations_data:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")
        return None

    headers = await db_get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    try:
        dataframe = DataFrame(violations_data, columns=clean_headers)
        return dataframe
    except Exception as err:
        logger.error(f"create_dataframe {repr(err)}")
        return None


async def get_now() -> str:
    """Возвращает текущую дату и время.
    :return: str
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def say_fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


async def test():
    await call_correct_acts(user_id='373084462')


if __name__ == '__main__':
    asyncio.run(test())
