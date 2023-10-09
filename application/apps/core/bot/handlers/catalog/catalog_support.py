from __future__ import annotations

import math
import os

import pandas as pd
from pandas import DataFrame

from apps.MyBot import bot_send_message
from apps.core.bot.handlers.catalog.catalog_func_handler import catalog_spot_data
from apps.core.bot.handlers.correct_entries.correct_support import check_dataframe
from apps.core.bot.messages.messages import Messages

list_number = 0
level_1_column = 3
level_2_column = 4
level_3_column = 5
level_4_column = 6


async def get_dataframe(hse_user_id: str | int, column_number: int = None) -> DataFrame | None:
    """

    :return:
    """
    file_list: list = await get_file_xlsx()
    if not file_list:
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены file_list')
        return None

    datadict: dict = pd.read_excel(file_list[-1], sheet_name=None)
    if not datadict:
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены datadict')
        return None

    dataframe: DataFrame = datadict[list(datadict.keys())[column_number]]
    if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
        return None

    return dataframe


async def get_level_1_list_dict(hse_user_id, dataframe: DataFrame = None):
    """

    :param dataframe:
    :param hse_user_id:
    :return:
    """
    if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
        dataframe = await get_dataframe(hse_user_id, column_number=list_number)
        if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
            await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
            return

    level_1: list = dataframe[dataframe.columns[level_1_column]].unique().tolist()
    if not level_1:
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены level_1')
        return

    d_list: list = [{f"level_1__{num}": item} for num, item in enumerate(level_1, start=1) if item is not None]
    return d_list


async def get_level_2_list_dict(hse_user_id, dataframe: DataFrame = None):
    """

    :param dataframe:
    :param hse_user_id:
    :return:
    """
    if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
        dataframe = await get_dataframe(hse_user_id, column_number=list_number)
        if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
            await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
            return

    df_level_2: DataFrame = dataframe.loc[
        dataframe[dataframe.columns[level_1_column]] == catalog_spot_data['level_1_name']]

    level_2: list = df_level_2[df_level_2.columns[level_2_column]].unique().tolist()
    if not level_2:
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены level_2')
        return []

    d_list: list = [{f"level_2__{num}": item} for num, item in enumerate(level_2, start=1) if item is not None]
    return d_list


async def text_processor_level(table_dataframe: DataFrame, nan_value: str = None, level: int = 0,
                               level_name: str = None) -> str:
    """Формирование текста для отправки пользователю

    """
    unique_items_titles: list = table_dataframe[table_dataframe.columns[level]].unique().tolist()

    items_text_list: list = []
    for i, (item_title) in enumerate(unique_items_titles, 1):
        item_info: str = f'level_{level + 1}__{i} : {item_title}'
        items_text_list.append(item_info)

    items_text: str = '\n'.join(items_text_list)

    header_text: str = Messages.Choose.choose_value
    footer_text: str = 'Нажмите на кнопку с номером выбранного значения'

    fin_list: list = [header_text, level_name, nan_value, items_text, footer_text]
    final_text = '\n\n'.join([item for item in fin_list if item])
    return final_text


async def text_processor(text: str = None) -> list:
    """Принимает data_list_to_text[] для формирования текста ответа
    Если len(text) <= 3500 - отправляет [сообщение]
    Если len(text) > 3500 - формирует list_with_parts_text = []

    :param text:
    :return: list - list_with_parts_text
    """
    if not text:
        return []

    step = 3500
    if len(text) <= step:
        return [text]

    len_parts = math.ceil(len(text) / step)
    list_with_parts_text: list = [text[step * (i - 1):step * i] for i in range(1, len_parts + 1)]

    return list_with_parts_text


async def get_file_xlsx() -> list:
    """Получение файлов со штатным расписанием в текущей директории

    """
    file_list: list = []

    for root, _, files in os.walk("."):
        for filename in files:
            if '.xlsx' in filename and 'constractor' in filename:
                file_list.append(f"{root}\\{filename}")
    return file_list


async def get_nan_value_text(hse_user_id, dataframe: DataFrame, column_nom: int = 0, level: int = 1) -> str:
    """

    :return:
    """

    nan_value_df: DataFrame = dataframe.loc[dataframe[dataframe.columns[column_nom]].isna()]
    if not await check_dataframe(nan_value_df, hse_user_id=hse_user_id):
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
        return ''

    items_text_list: list = []
    for index, row in nan_value_df.iterrows():
        department = row.get("Подразделение полностью", " - ")
        job_title = row.get("Должность")
        employee = row.get("Сотрудник")
        personnel_number = row.get("Табельный номер")
        e_mail = row.get("Почта")
        phone_number = row.get("Тел")

        item_info: str = f'{department}\n{job_title} {employee} \nтаб.ном {personnel_number}\ne-mail {e_mail}\nтел {phone_number}'
        await bot_send_message(chat_id=hse_user_id, text=item_info)

        items_text_list.append(item_info)

    items_text: str = '\n\n'.join([item for item in items_text_list if item is not None])

    return items_text


async def check_dataframe(dataframe: DataFrame, hse_user_id: str | int) -> bool:
    """Проверка dataframe на наличие данных

    :param dataframe:
    :param hse_user_id: id пользователя
    :return:
    """
    if dataframe is None:
        text_violations: str = 'не удалось получить данные!'
        logger.error(f'{hse_user_id = } {text_violations}')
        return False

    if dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}')
        return False

    return True
