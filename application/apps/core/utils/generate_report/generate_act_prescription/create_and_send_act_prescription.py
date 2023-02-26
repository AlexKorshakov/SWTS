import asyncio
import traceback
from datetime import datetime
from pprint import pprint

from pandas import DataFrame

from apps.MyBot import MyBot
from apps.core.bot.bot_utils.progress_bar import ProgressBar
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import db_get_period_for_current_week
from apps.core.database.query_constructor import QueryConstructor
from apps.core.utils.data_recording_processor.set_user_report_data import set_act_data_on_google_drive
from apps.core.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.utils.generate_report.generate_act_prescription.create_act_prescription import create_act_prescription
from apps.core.utils.generate_report.generator_report import get_act_number_on_data_base, set_act_data_on_data_base
from apps.core.utils.generate_report.get_report_path import get_and_create_full_act_prescription_name
from apps.core.utils.generate_report.send_report_from_user import send_report_from_user
from apps.core.utils.reports_processor.report_worker_utils import format_data_db, get_clean_headers, get_query, \
    get_clear_list_value, get_general_constractor_list, create_lite_dataframe_from_query, get_general_constractor_data
from apps.core.utils.secondary_functions.get_part_date import get_week_message, get_year_message
from loader import logger


async def create_and_send_act_prescription(chat_id: int, query_act_date_period=None, **kwargs) -> bool:
    """Формирование актов - предписаний за период query_act_date_period по организации

    :param query_act_date_period: list период (даты) для выборки
    :param chat_id: id  пользователя
    :return:
    """

    msg = await MyBot.bot.send_message(chat_id=chat_id, text='⬜' * 10)
    p_bar = ProgressBar(msg=msg)

    # # await p_bar.start()
    # await p_bar.update_msg(3)
    # await p_bar.update_msg(7)
    # await p_bar.finish()

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

    await p_bar.update_msg(3)
    clear_list_value = await get_clean_data(chat_id, query_act_date_period, headers=clean_headers)
    if not clear_list_value:
        return False

    await p_bar.update_msg(4)
    general_constractor_ids_list: list = await get_general_constractor_list(clear_list_value=clear_list_value)
    if not general_constractor_ids_list:
        return False

    await p_bar.update_msg(5)
    for constractor_id in general_constractor_ids_list:

        act_dataframe: DataFrame = await get_act_dataframe(
            chat_id=chat_id, act_period=query_act_date_period, constractor_id=constractor_id, headers=clean_headers
        )
        if act_dataframe.empty:
            continue

        act_number: int = await get_act_number_on_data_base()
        if not act_number:
            act_number: str = '00000'
        await p_bar.update_msg(6)
        full_act_prescription_path: str = await get_full_act_prescription_path(
            chat_id=chat_id, act_number=act_number, act_date=act_date, constractor_id=constractor_id
        )
        if not full_act_prescription_path:
            continue

        act_is_created: bool = await create_act_prescription(
            chat_id=chat_id, act_number=act_number, dataframe=act_dataframe,
            full_act_path=full_act_prescription_path, act_date=act_date
        )
        if not act_is_created:
            continue

        await p_bar.update_msg(7)
        await MyBot.bot.send_message(
            chat_id=chat_id, text=f'{Messages.Report.create_successfully} \n'
        )

        await set_act_data_on_data_base(
            act_data=act_dataframe, act_num=act_number, act_date=act_date
        )
        await p_bar.update_msg(8)
        await set_act_data_on_google_drive(
            chat_id=chat_id, full_report_path=full_act_prescription_path
        )

        await p_bar.update_msg(9)
        await send_act_prescription(chat_id, full_act_prescription_path)

        await MyBot.bot.send_message(
            chat_id=chat_id, text=f'{Messages.Report.done} \n'
        )
        await p_bar.update_msg(10)

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
    print(f'{__name__} {say_fanc_name()} {query}')

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

    await convert_report_to_pdf(
        chat_id=chat_id, path=full_act_prescription_path
    )
    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_act_prescription_path
    )
    full_act_prescription_path = full_act_prescription_path.replace(".xlsx", ".pdf")

    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_act_prescription_path
    )
    return True


def say_fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


async def test():
    chat_id = 579531613

    now = datetime.now()

    current_week: str = await get_week_message(current_date=now)
    current_year: str = await get_year_message(current_date=now)

    act_date_period = await db_get_period_for_current_week(current_week, current_year)
    pprint(f"{act_date_period = }")

    #  act_date_period = now

    await create_and_send_act_prescription(chat_id, act_date_period)


if __name__ == "__main__":
    asyncio.run(test())
