from __future__ import annotations

import asyncio
import math
from datetime import datetime
from itertools import chain

from aiogram import types
from aiogram.dispatcher import FSMContext
from pandas import DataFrame, Timestamp

from apps.MyBot import MyBot, bot_send_message
from apps.core.bot.filters.custom_filters import is_private
from apps.core.bot.handlers.catalog.catalog_support import get_dataframe, list_number
from apps.core.bot.messages.messages import Messages
from apps.core.bot.states.CatalogState import CatalogStateEmployee
from loader import logger


@MyBot.dp.message_handler(is_private, state=CatalogStateEmployee.all_states)
async def catalog_data_all_states_answer(message: types.Message = None, state: FSMContext = None,
                                         user_id: int | str = None, text: str = None):
    """Обработка изменений

    :param text:
    :param user_id:
    :param message:
    :param state:
    :return:
    """
    hse_user_id = message.chat.id if message else user_id
    logger.debug(f'{hse_user_id = } {message.text = }')
    logger.info(f'{hse_user_id = } {message.text = }')

    await state.finish()

    dataframe: DataFrame = await get_dataframe(hse_user_id, column_number=list_number)
    if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
        return

    text_too_search: str = message.text if message else text

    await text_processor_for_text_query(hse_user_id, dataframe, text_too_search=text_too_search)


async def text_processor_for_text_query(hse_user_id: str | int, table_dataframe: DataFrame,
                                        text_too_search: str) -> str:
    """Формирование текста для отправки пользователю

    """
    items_text_list: list = []

    if not text_too_search:
        return 'данные не найдены'

    try:
        text_too_search: int = int(text_too_search)

    except ValueError as err:
        logger.info(f'{hse_user_id = } {text_too_search = } {repr(err)}')

    if isinstance(text_too_search, int):
        items_text_list: list = await processor_search_if_int(table_dataframe, text_too_search)

    if isinstance(text_too_search, str):
        items_text_list: list = await processor_search_if_str(table_dataframe, text_too_search)

    if not items_text_list:
        await bot_send_message(chat_id=hse_user_id, text='Данные запроса не найдены')
        return ''

    items_text: str = await prepare_text(hse_user_id, items_text_list)

    return items_text


async def prepare_text(hse_user_id: str | int, data: list) -> str:
    """

    :param hse_user_id:
    :param data:
    :return:
    """
    text: str = ''
    if not isinstance(data, list):
        return ''

    dat_list: list = list(chain(*data))
    if not dat_list:
        return text

    for num, item in enumerate(dat_list, start=1):
        if num == 10:
            await bot_send_message(chat_id=hse_user_id, text='уточните поиск и повторите')
            return ''

        await bot_send_message(
            chat_id=hse_user_id,
            text=f'Найденов столбце: {list(item.keys())[0]} : {list(item.values())[0]}'
        )


async def processor_search_if_int(table_dataframe: DataFrame, text_too_search: int) -> list:
    """

    :param table_dataframe:
    :param text_too_search:
    :return:
    """
    items_text_list_list: list = []

    for col_item in table_dataframe.columns.values.tolist()[0:1]:
        df_res: DataFrame = table_dataframe.loc[table_dataframe[col_item] == int(text_too_search)]

        df_headers: list = list(df_res.columns)[12:]
        items_text_list: list = await get_list_text(df_res, df_headers, col_item)

        if items_text_list:
            items_text_list_list.append(items_text_list)

    return items_text_list_list


async def processor_search_if_str(table_dataframe: DataFrame, text_too_search: str) -> list:
    """

    :param table_dataframe:
    :param text_too_search:
    :return:
    """
    items_text_list_list: list = []

    for num_col, col_item in enumerate(table_dataframe):
        if num_col == 7: break

        mask = table_dataframe[col_item].str.contains(f"{text_too_search}", case=False, regex=True, na=False)

        df_res: DataFrame = table_dataframe.loc[mask]

        df_headers: list = list(df_res.columns)[12:]
        items_text_list: list = await get_list_text(df_res, df_headers, col_item)

        if items_text_list:
            items_text_list_list.append(items_text_list)

    return items_text_list_list


async def get_list_text(df_res, df_headers, col_item) -> list:
    """

    :param df_res:
    :param df_headers:
    :param col_item:
    :return:
    """
    items_text_list = []
    for _, row in df_res.iterrows():
        department = row.get("Подразделение полностью", " - ")
        job_title = row.get("Должность", " - ")
        employee = row.get("Сотрудник", " - ")
        personnel_number = row.get("Табельный номер", " - ")
        e_mail = row.get("Почта", " - ")
        phone_number = row.get("Тел", " - ")
        supervisor = row.get("Руководитель", " - ")

        headers_list_str: list = []
        # if admin:
        for header in df_headers:
            i_char = row.get(header) if isinstance(row.get(header), Timestamp) else None
            if i_char:
                headers_list_str.append(f"{header}: {i_char.strftime('%d.%m.%Y')}")

        headers_str = ' \n'.join(headers_list_str)

        item_info: str = f'{department}\n\n{job_title} {employee} \n\nтаб.ном {personnel_number}\n' \
                         f'e-mail {e_mail}\nтел {phone_number}\n\nРуководитель\n{supervisor}'
        if headers_str:
            item_info = f'{item_info}\n\nАттестации по Промышленной безопасности:\n{headers_str}'

        items_text_list.append(
            {col_item: item_info}
        )

    return items_text_list


async def text_processor(text: str = None) -> list:
    """Принимает data_list_to_text[] для формирования текста ответа
    Если len(text) <= 3500 - отправляет [сообщение]
    Если len(text) > 3500 - формирует list_with_parts_text = []

    :param text:
    :return: list - list_with_parts_text
    """
    if not text:
        return []

    step: int = 3500
    if len(text) <= step:
        return [text]

    len_parts = math.ceil(len(text) / step)
    list_with_parts_text: list = [text[step * (i - 1):step * i] for i in range(1, len_parts + 1)]

    return list_with_parts_text


async def get_now() -> str:
    """Возвращает текущую дату и время.

    :return: str
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


async def check_dataframe(dataframe: DataFrame, hse_user_id: str | int) -> bool:
    """Проверка dataframe на наличие данных

    :param dataframe:
    :param hse_user_id: id пользователя
    :return:
    """
    if dataframe is None:
        text_violations: str = 'не удалось получить данные!'
        logger.error(f'{hse_user_id = } {text_violations}')
        # await bot_send_message(chat_id=hse_user_id, text=text_violations)
        return False

    if dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}')
        return False

    return True


async def test():
    message: types.Message = None
    state: FSMContext = CatalogStateEmployee
    user_id: int | str = 373084462
    text: str = '3526'

    await catalog_data_all_states_answer(message, state, user_id, text)


if __name__ == '__main__':
    asyncio.run(test())
