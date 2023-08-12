from __future__ import annotations

import asyncio
import traceback
from itertools import chain

from aiogram import types
from pandas import DataFrame

from apps.MyBot import bot_send_message, bot_send_document
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages_test import msg
from config.config import MAIN_DIR


async def qr_matrix_nom_processing(hse_user_id, qr_data):
    """"""
    matrix_path = f'{MAIN_DIR}apps\\core\\bot\\handlers\\photo\\isolation_matrix\\'

    matrix_data = [
        {
            "file": "матрица изоляции CM51-PU-002.docx",
            "matrix_code": 'CM51-PU-002',
            "matrix_post": 'CM51-PU-003',
            "matrix_prev": 'CM51-PU-001',
            "main_location": 'Участки технологического комплекса',
            "glob_location": 'УАВиН',
            "location": 'литер здания',
            "sub_location": 'участок или площадка',
            "description": 'Насос шламовый Warman 10/8F-AH/WRT',
            "technology": 'как то работает и ладно',
            "responsible": 'Иванов Петр Сидорович',
            "subdir": 'C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\apps\\core\\bot\\handlers\\photo\\isolation_matrix\\Все матрицы\\Участки технологического комплекса\\УАВиН\\Матрицы УАВиН\\Выщелачивание',

        },
    ]

    for item in matrix_data:
        if item.get('matrix_code') != list(chain(*qr_data))[0].replace('qr_matrix_nom_', ''): continue

        reply_markup = await add_employee_inline_keyboard_with_action(item)

        doc_path: str = f"{item.get('subdir')}\\{item.get('file')}"
        caption: str = f"{item.get('main_location')} " \
                       f"{item.get('glob_location')} " \
                       f"{item.get('location')} " \
                       f"{item.get('sub_location')} " \
                       f"Установка: {item.get('description')}\n" \
                       f"Ответственный: {item.get('responsible')}\n" \
                       f"Технология: {item.get('technology')}"

        kwargs: dict = {
            'reply_markup': reply_markup
        }

        await bot_send_document(
            chat_id=hse_user_id,
            doc_path=doc_path,
            caption=caption,
            fanc_name=await fanc_name(),
            **kwargs
        )
        print()


async def add_employee_inline_keyboard_with_action(item: dict):
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    if item.get("matrix_code"):
        markup.add(types.InlineKeyboardButton(
            text='Матрица изоляции',
            callback_data=posts_cb.new(id='-', action='еquipment_matrix_doc')))

    if item.get("matrix_post"):
        markup.add(types.InlineKeyboardButton(
            text='Следующая установка',
            callback_data=posts_cb.new(id='-', action='еquipment_matrix_next')))

    if item.get("matrix_prev"):
        markup.add(types.InlineKeyboardButton(
            text='Предыдущая установка',
            callback_data=posts_cb.new(id='-', action='еquipment_matrix_prev')))

    markup.add(types.InlineKeyboardButton(
        text='Параметры работы оборудования',
        callback_data=posts_cb.new(id='-', action='еquipment_operation_parameters')))

    markup.add(types.InlineKeyboardButton(
        text='Заявка на ремонт',
        callback_data=posts_cb.new(id='-', action='equipment_repair_request')))

    markup.add(types.InlineKeyboardButton(
        text='Заказать пиццу',
        callback_data=posts_cb.new(id='-', action='ORDER_PIZZA')))

    return markup


# answer_text: str = await generate_text(hse_user_id, qr_data=data)
#
# if not answer_text:
#     answer_text: str = await msg(
#         hse_user_id, cat='warning', msge='qr_not_found', default="QR-код, не распознан или отсутствует").g_mas()
#     await bot_send_message(chat_id=hse_user_id, text=answer_text)
#
# for item_txt in await text_processor(text=answer_text):
#     await bot_send_message(chat_id=hse_user_id, text=item_txt)


# async def text_processor(text: str = None) -> list:
#     """Принимает data_list_to_text[] для формирования текста ответа
#     Если len(text) <= 3500 - отправляет [сообщение]
#     Если len(text) > 3500 - формирует list_with_parts_text = []
#
#     :param text:
#     :return: list - list_with_parts_text
#     """
#     if not text:
#         return []
#
#     step = 3500
#     if len(text) <= step:
#         return [text]
#
#     len_parts = math.ceil(len(text) / step)
#     list_with_parts_text: list = [text[step * (i - 1):step * i] for i in range(1, len_parts + 1)]
#
#     return list_with_parts_text
#
#
# async def generate_text(hse_user_id: str | int, qr_data: str | list = None) -> str:
#     """Получение информации из data
#
#     :param hse_user_id:
#     :param qr_data:
#     :return:
#     """
#     if qr_data is None:
#         return ""
#
#     qr_data_list: list = []
#     if isinstance(qr_data, list):
#         qr_data_list: list = list(chain(*qr_data))
#
#     qr_data_text: list = []
#     for qr_data_item in qr_data_list:
#
#         if isinstance(qr_data_item, str):
#             qr_data_list: list = qr_data_item.split("_")
#             if qr_data_list[0] != 'qr':
#                 return ''
#
#             if len(qr_data_list) < 3:
#                 return ''
#
#             act_number = qr_data_list[-1]
#             user_id = qr_data_list[-2]
#
#             violations_df: DataFrame = await get_violations_df(act_number)
#             if not await check_dataframe(violations_df, hse_user_id=hse_user_id):
#                 await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
#                 continue
#
#             act_text: str = await text_processor_act(act_number, violations_df)
#             items_text: str = await text_processor_items(violations_df, hse_user_id=user_id)
#
#             qr_data_text.append(f'{act_text}\n\n{items_text}')
#
#     return '\n\n '.join(qr_data_text)

async def test():
    hse_user_id = 373084462
    data = [['qr_matrix_nom_CM51-PU-002']]
    await qr_matrix_nom_processing(hse_user_id, data)


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


if __name__ == '__main__':
    asyncio.run(test())
