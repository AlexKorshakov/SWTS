from __future__ import annotations
import asyncio
import traceback
from datetime import datetime

from pandas import DataFrame

from apps.MyBot import bot_send_message, _send_message
from apps.core.bot.bot_utils.progress_bar import ProgressBar
from apps.core.bot.handlers.correct_entries.correct_support import check_dataframe
from apps.core.bot.handlers.photo.AmazingQRCodeGenerator import create_qr_code, create_qr_code_with_param
from apps.core.bot.messages.messages import Messages
from apps.core.database.query_constructor import QueryConstructor
from apps.core.utils.data_recording_processor.set_user_report_data import set_act_data_on_google_drive, \
    set_act_data_on_data_in_registry
from apps.core.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.utils.generate_report.generate_act_prescription.create_act_prescription import create_act_prescription
from apps.core.utils.generate_report.generator_report import get_act_number_on_data_base, set_act_data_on_data_base
from apps.core.utils.generate_report.get_report_path import get_and_create_full_act_prescription_name, \
    get_and_create_full_act_prescription_name_in_registry, get_full_qr_report_path
from apps.core.utils.generate_report.send_report_from_user import send_report_from_user
from apps.core.utils.reports_processor.report_worker_utils import format_data_db, get_clean_headers, get_query, \
    get_clear_list_value, get_general_constractor_list, create_lite_dataframe_from_query, get_general_constractor_data
from apps.core.utils.secondary_functions.get_filepath import get_report_full_filepath
from loader import logger


async def create_and_send_act_prescription(chat_id: int, query_act_date_period=None, **kwargs) -> bool:
    """Формирование актов - предписаний за период query_act_date_period по организации

    :param query_act_date_period: list период (даты) для выборки
    :param chat_id: id  пользователя
    :return:
    """

    msg = await _send_message(chat_id=chat_id, text='⬜' * 10)
    p_bar = ProgressBar(msg=msg)

    await p_bar.update_msg(1)
    act_kwargs = {**kwargs}
    if act_kwargs:
        logger.info(f"{act_kwargs = }")

    act_date: str = datetime.now().strftime("%d.%m.%Y")  # '28.10.2022'  #

    await p_bar.update_msg(2)
    if not query_act_date_period:
        date_now = await format_data_db(act_date)
        query_act_date_period = [date_now, date_now]

    clean_headers: list = await get_clean_headers(table_name='core_violations')

    clear_list_value = await get_clean_data(chat_id, query_act_date_period, headers=clean_headers)
    if not clear_list_value:
        return False

    await p_bar.update_msg(3)
    general_constractor_ids_list: list = await get_general_constractor_list(clear_list_value=clear_list_value)
    if not general_constractor_ids_list:
        return False

    await p_bar.update_msg(4)
    for constractor_id in general_constractor_ids_list:

        act_dataframe: DataFrame = await get_act_dataframe(
            chat_id=chat_id, act_period=query_act_date_period, constractor_id=constractor_id, headers=clean_headers
        )
        if not await check_dataframe(act_dataframe, chat_id):
            continue

        act_number: int = await get_act_number_on_data_base()
        if not act_number:
            act_number: str = '00000'

        full_act_prescription_path: str = await get_full_act_prescription_path(
            chat_id=chat_id, act_number=act_number, act_date=act_date, constractor_id=constractor_id
        )

        qr_report_path = await get_report_full_filepath(str(chat_id), actual_date=act_date)

        # full_qr_report_path: str = await get_full_qr_report_path(qr_report_path, chat_id, act_number)

        await create_qr_code_with_param(chat_id, act_number, qr_report_path)

        if not full_act_prescription_path:
            continue

        await p_bar.update_msg(5)
        act_is_created: bool = await create_act_prescription(
            chat_id=chat_id, act_number=act_number, dataframe=act_dataframe,
            full_act_path=full_act_prescription_path, act_date=act_date, qr_img_insert=True
        )
        if not act_is_created:
            continue

        await p_bar.update_msg(6)
        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.create_successfully} \n')

        await set_act_data_on_data_base(
            act_data=act_dataframe, act_num=act_number, act_date=act_date
        )
        await p_bar.update_msg(7)
        await set_act_data_on_google_drive(
            chat_id=chat_id, full_report_path=full_act_prescription_path
        )

        await p_bar.update_msg(8)
        path_in_registry = await get_full_patch_to_act_prescription(
            chat_id=chat_id, act_number=act_number, act_date=act_date, constractor_id=constractor_id
        )
        await set_act_data_on_data_in_registry(
            hse_chat_id=chat_id, act_dataframe=act_dataframe, path_in_registry=path_in_registry,
            act_date=act_date, act_number=act_number, constractor_id=constractor_id
        )

        await p_bar.update_msg(9)
        await send_act_prescription(
            chat_id=chat_id, full_act_prescription_path=full_act_prescription_path
        )

        await p_bar.update_msg(10)
        await bot_send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    return True


async def get_act_dataframe(chat_id, act_period, constractor_id, headers):
    """Получение dataframe с данными акта - предписания

    :return:
    """
    table_name: str = 'core_violations'

    # TODO заменить на вызов конструктора QueryConstructor
    query: str = await get_query(
        type_query='general_contractor_id', table_name=table_name, query_date=act_period,
        value_id=constractor_id, user_id=chat_id
    )
    # print(f'{__name__} {fanc_name()} {query}')

    act_dataframe: DataFrame = await create_lite_dataframe_from_query(
        chat_id=chat_id, query=query, clean_headers=headers
    )

    return act_dataframe


async def get_full_act_prescription_path(chat_id, act_number, act_date, constractor_id) -> str:
    """Получение и создание полного пути акта предписания

    """

    contractor_data: dict = await get_general_constractor_data(
        constractor_id=constractor_id, type_constractor='general'
    )
    if not contractor_data:
        return ''

    param: dict = {
        'act_number': act_number,
        'act_date': act_date,
        'general_contractor': contractor_data.get('title'),
        'short_title': contractor_data.get('short_title'),
    }
    full_act_prescription_path: str = await get_and_create_full_act_prescription_name(chat_id=chat_id, param=param)

    return full_act_prescription_path


async def get_full_patch_to_act_prescription(chat_id, act_number, act_date, constractor_id) -> str:
    """Формирование полного пути до папки хранения файла json акта - предписания

    :return:
    """
    contractor_data: dict = await get_general_constractor_data(
        constractor_id=constractor_id, type_constractor='general'
    )
    if not contractor_data:
        return ''

    param: dict = {
        'act_number': act_number,
        'act_date': act_date,
        'general_contractor': contractor_data.get('title'),
        'short_title': contractor_data.get('short_title'),
        'contractor_data': contractor_data,
    }
    full_act_prescription_path: str = await get_and_create_full_act_prescription_name_in_registry(
        chat_id=chat_id, param=param
    )

    return full_act_prescription_path


async def get_clean_data(chat_id, query_act_date_period, headers, **stat_kwargs):
    """Получение данных с заголовками за период query_act_date_period

    :return:
    """
    kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "period": query_act_date_period,
            "act_number": "",
            "location": stat_kwargs.get('location', None)
        }
    }
    query: str = await QueryConstructor(chat_id, table_name='core_violations', **kwargs).prepare_data()

    clear_list_value: list = await get_clear_list_value(
        chat_id=chat_id, query=query, clean_headers=headers
    )

    return clear_list_value


async def send_act_prescription(chat_id: int or str, full_act_prescription_path: str) -> bool:
    """Отправка акта-предписания пользователю в заданных форматах

    :param full_act_prescription_path: int or str
    :param chat_id: str
    :return:
    """

    # await convert_report_to_pdf(
    #     chat_id=chat_id, path=full_act_prescription_path
    # )
    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_act_prescription_path
    )
    # full_act_prescription_path = full_act_prescription_path.replace(".xlsx", ".pdf")
    #
    # await send_report_from_user(
    #     chat_id=chat_id, full_report_path=full_act_prescription_path
    # )
    return True



# async def set_act_prescription_in_registry(act_prescription_json) -> bool:
#     """Добавление акта-предписания в хранилище (реестр) актов
#
#     :return:
#     """
#
#     # set_json
#     #
#     # set_xlsx
#     #
#     # set_pdf
#
#     return True
#

# async def set_json_act_prescription_in_registry(full_patch: str, json_name: str, json_data) -> bool:
#     """
#
#     :param json_name:
#     :param full_patch:
#     :return:
#     """
#     with open(f'{full_patch}\\{json_name}', 'w') as json_file:
#         json_file.write(json_data)
#
#     return True


def say_fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


async def test():
    chat_id = 373084462

    # now = datetime.now()
    #
    # current_week: str = await get_week_message(current_date=now)
    # current_year: str = await get_year_message(current_date=now)
    #
    # act_date_period = await db_get_period_for_current_week(current_week, current_year)
    # pprint(f"{act_date_period = }")
    #
    #  act_date_period = now
    #
    # await create_and_send_act_prescription(chat_id, act_date_period)

    act_number = 1100000
    act_date = datetime.now().strftime("%d.%m.%Y")
    constractor_id = 1

    await get_full_patch_to_act_prescription(chat_id, act_number, act_date, constractor_id)


if __name__ == "__main__":
    asyncio.run(test())
