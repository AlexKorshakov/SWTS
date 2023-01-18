import asyncio
from datetime import datetime
from pprint import pprint

from pandas import DataFrame
from apps.MyBot import MyBot
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import db_get_period_for_current_week
from apps.core.utils.data_recording_processor.set_user_report_data import set_report_data
from apps.core.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.utils.generate_report.generate_act_prescription.create_and_send_act_prescription import get_clean_data
from apps.core.utils.generate_report.generate_daily_report.create_daily_report import create_daily_report
from apps.core.utils.generate_report.get_report_path import get_full_daily_report_name
from apps.core.utils.generate_report.send_report_from_user import send_report_from_user
from apps.core.utils.reports_processor.report_worker_utils import format_data_db, get_query, \
    create_lite_dataframe_from_query
from apps.core.utils.secondary_functions.get_part_date import get_week_message, get_year_message
from loader import logger


async def create_and_send_daily_report(chat_id, query_act_date_period: list = None, **kwargs) -> bool:
    """Формирование и отправка отчета

    :param query_act_date_period:
    :param chat_id:
    :return:
    """

    daily_report_date: str = datetime.now().strftime("%d.%m.%Y")  # '28.10.2022'  #

    if not query_act_date_period:
        query_act_date_period = await format_data_db(daily_report_date)

    type_query = 'query_daily_report'
    clean_headers, clear_list_value = await get_clean_data(chat_id, query_act_date_period, type_query)
    if not clear_list_value:
        return False

    full_daily_report_path: str = await get_full_daily_report_name(chat_id=chat_id)

    daily_report_dataframe: DataFrame = await get_daily_report_dataframe(
        chat_id=chat_id, act_period=query_act_date_period, headers=clean_headers
    )

    if daily_report_dataframe.empty:
        logger.error(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return False

    act_is_created: bool = await create_daily_report(
        chat_id=chat_id,
        dataframe=daily_report_dataframe,
        full_daily_report_report_path=full_daily_report_path
    )

    if not act_is_created:
        return False

    await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    await send_daily_report(chat_id=chat_id, full_report_path=full_daily_report_path)

    return True


async def get_daily_report_dataframe(chat_id, act_period, headers):
    """Получение dataframe с данными акта - предписания

    :return:
    """
    table_name: str = 'core_violations'

    query: str = await get_query(
        type_query='query_daily_report', table_name=table_name, query_date=act_period, user_id=chat_id
    )

    print(f'get_daily_report_dataframe {query = }')

    act_dataframe: DataFrame = await create_lite_dataframe_from_query(
        chat_id=chat_id, query=query, clean_headers=headers
    )
    return act_dataframe


async def send_daily_report(chat_id: str, full_report_path: str):
    """Отправка отчета пользователю в заданных форматах

    :return:
    """

    await convert_report_to_pdf(
        chat_id=chat_id, path=full_report_path
    )
    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_report_path
    )
    full_act_prescription_path = full_report_path.replace(".xlsx", ".pdf")

    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_act_prescription_path
    )


async def test():
    chat_id = 373084462

    now = datetime.now()

    current_week: str = await get_week_message(current_date=now)
    current_year: str = await get_year_message(current_date=now)

    act_date_period = await db_get_period_for_current_week(current_week, current_year)
    pprint(f"{act_date_period = }")

    await create_and_send_daily_report(chat_id, act_date_period)


if __name__ == "__main__":
    asyncio.run(test())
