from __future__ import annotations
import asyncio
from datetime import datetime

from aiogram import types
from pandas import DataFrame

from apps.MyBot import MyBot, bot_send_message
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb, build_inlinekeyboard
from apps.core.bot.messages.messages import Messages, LogMessage
from apps.core.database.db_utils import db_get_table_headers, db_get_data_list, db_get_data_dict_from_table_with_id
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_act_item_correct']))
async def call_correct_act_item_correct(call: types.CallbackQuery = None, callback_data: dict[str, str] = None,
                                        user_id: int | str = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """

    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')
    logger.debug(f'{callback_data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    if not call:
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_call)
        return

    if not call.message.values['text']:
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_call_text)
        return

    act_number_text = call.message.values['text'].split('_')[-1]
    logger.debug(f'{hse_user_id = } {act_number_text = }')

    try:
        act_number_text = int(act_number_text)
    except Exception as err:
        logger.error(f'{hse_user_id = } {repr(err)} {act_number_text = }')
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_command)
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)
        return

    query_kwargs: dict = {
        "action": 'SELECT', "subject": '*',
        "conditions": {
            "act_number": act_number_text,
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    violations_dataframe: DataFrame = await create_lite_dataframe_from_query(query=query, table_name='core_violations')
    if violations_dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}  \n{query = }')
        return

    reply_markup: types.InlineKeyboardMarkup = await add_correct_item_inline_keyboard_with_action(violations_dataframe)

    text_violations: str = await text_processor_items_act_violations(violations_dataframe, act_number_text)

    await bot_send_message(chat_id=hse_user_id, text=text_violations, reply_markup=reply_markup)

    return True


@MyBot.dp.callback_query_handler(lambda call: 'item_number_' in call.data)
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

    markup.add(types.InlineKeyboardButton('Финализировать и записать пункт',
                                          callback_data=posts_cb.new(id='-', action='correct_act_item_finalize')))
    markup.add(types.InlineKeyboardButton('Исправить данные пункта',
                                          callback_data=posts_cb.new(id='-', action='correct_act_item_data_correct')))
    markup.add(types.InlineKeyboardButton('Удалить пункт',
                                          callback_data=posts_cb.new(id='-', action='correct_act_item_delete')))
    return markup


async def text_processor_items_act_violations(user_violations_df: DataFrame, act_number: str | int) -> str:
    """Формирование текста для отправки пользователю"""

    unique_items_ids: list = user_violations_df.id.unique().tolist()

    items_description: list = []
    len_unique_acts: int = 0

    for item_id in unique_items_ids:

        if not act_number:
            continue

        item_violations_dataframe = user_violations_df.copy(deep=True)
        item_df = item_violations_dataframe.loc[item_violations_dataframe['id'] == item_id]

        if item_violations_dataframe.empty:
            logger.error(f'{Messages.Error.dataframe_is_empty}')
            continue

        created_at = item_df['created_at'].values[0]
        item_status = await get_item_title_for_id(
            'core_status', item_id=item_df['status_id'].values[0]
        )
        item_main_category = await get_item_title_for_id(
            table_name='core_maincategory', item_id=item_df['main_category_id'].values[0]
        )
        item_category = await get_item_title_for_id(
            table_name='core_category', item_id=item_df['category_id'].values[0]
        )
        item_general_contractor_id = await get_item_title_for_id(
            table_name='core_generalcontractor', item_id=item_df['general_contractor_id'].values[0]
        )
        item_main_location = await get_item_title_for_id(
            table_name='core_mainlocation', item_id=item_df['main_location_id'].values[0]
        )
        item_sub_location = await get_item_title_for_id(
            table_name='core_sublocation', item_id=item_df['sub_location_id'].values[0]
        )
        item_description = item_df['description'].values[0]
        elimination_time = await get_item_title_for_id(
            table_name='core_eliminationtime', item_id=item_df['elimination_time_id'].values[0]
        )
        normative_documents_title = await get_item_title_for_id(
            table_name='core_normativedocuments', item_id=item_df['normative_documents_id'].values[0],
        )

        normative_documents_desc = await get_item_title_for_id(
            table_name='core_normativedocuments', item_id=item_df['normative_documents_id'].values[0],
            item_name='normative'
        )

        item_info = f'Ном: {item_id} от {created_at} Статус: {item_status} \n' \
                    f'Устранить до: {elimination_time} ' \
                    f'Подрядчик: {item_general_contractor_id} \n' \
                    f'Территория: {item_main_location} - {item_sub_location} \n' \
                    f'Направление: {item_main_category} - Категория: {item_category}\n' \
                    f'Описание: {item_description} \n' \
                    f'Подкатегория: {normative_documents_title} ' \
                    f'Нормативка: {normative_documents_desc}\n'

        items_description.append(item_info)
        len_unique_acts += 1

    items_text: str = '\n'.join(items_description)

    header_text: str = f'Пункты акта {act_number} : Всего пунктов {len_unique_acts}'
    final_text: str = f'{header_text} \n\n{items_text}'
    return final_text


async def get_item_title_for_id(table_name: str, item_id: int, item_name: str = None) -> str:
    """

    :param item_name:
    :param table_name:
    :param item_id:
    :return:
    """
    item_dict: dict = await db_get_data_dict_from_table_with_id(
        table_name=table_name,
        post_id=item_id
    )

    item_name = item_name if item_name else 'title'
    item_text: str = item_dict.get(item_name, '')
    return item_text


async def add_correct_item_inline_keyboard_with_action(user_violations: DataFrame):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    unique_acts_numbers: list = user_violations.id.unique().tolist()
    unique_acts_numbers: list = [f'item_number_{item}' for item in unique_acts_numbers if item]

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = unique_acts_numbers
    count_col = board_config.count_col = 2

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level)

    return reply_markup


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


async def test():
    await call_correct_act_item_correct(user_id='373084462')


if __name__ == '__main__':
    asyncio.run(test())
