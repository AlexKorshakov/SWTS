import asyncio
from datetime import datetime
from pprint import pprint

from pandas import DataFrame

from apps.MyBot import MyBot
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import db_get_period_for_current_week
from apps.core.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.utils.generate_report.generate_act_prescription.create_and_send_act_prescription import get_clean_data
from apps.core.utils.generate_report.generate_stat.create_stat import create_stat
from apps.core.utils.generate_report.get_report_path import get_full_stat_name
from apps.core.utils.generate_report.send_report_from_user import send_report_from_user
from apps.core.utils.reports_processor.report_worker_utils import format_data_db, get_query, \
    create_lite_dataframe_from_query
from apps.core.utils.secondary_functions.get_part_date import get_week_message, get_year_message
from loader import logger


async def create_and_send_stat(chat_id, query_stat_date_period: list = None, **kwargs) -> bool:
    """Формирование и отправка отчета

    :param query_stat_date_period:
    :param chat_id:
    :return:
    """

    stat_date: str = datetime.now().strftime("%d.%m.%Y")  # '28.10.2022'  #

    if not query_stat_date_period:
        query_stat_date_period = await format_data_db(stat_date)

    type_query = 'query_stat'
    clean_headers, clear_list_value = await get_clean_data(chat_id, query_stat_date_period, type_query)
    if not clear_list_value:
        return False

    full_stat_path: str = await get_full_stat_name(chat_id=chat_id)

    stat_dataframe: DataFrame = await get_stat_dataframe(
        chat_id=chat_id, stat_period=query_stat_date_period, headers=clean_headers
    )

    if stat_dataframe.empty:
        logger.error(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return False

    stat_is_created: bool = await create_stat(
        chat_id=chat_id,
        dataframe=stat_dataframe,
        full_stat_path=full_stat_path
    )

    if not stat_is_created:
        return False

    await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    await send_stat(chat_id=chat_id, full_report_path=full_stat_path)

    return True


async def get_stat_dataframe(chat_id, stat_period, headers):
    """Получение dataframe с данными статистики

    :return:
    """
    table_name: str = 'core_violations'

    query: str = await get_query(
        type_query='query_stat', table_name=table_name, query_date=stat_period, user_id=chat_id
    )

    print(f'get_stat_dataframe {query = }')

    stat_dataframe: DataFrame = await create_lite_dataframe_from_query(
        chat_id=chat_id, query=query, clean_headers=headers
    )
    return stat_dataframe


async def send_stat(chat_id: str, full_report_path: str):
    """Отправка отчета пользователю в заданных форматах

    :return:
    """

    await convert_report_to_pdf(
        chat_id=chat_id, path=full_report_path
    )
    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_report_path
    )
    full_stat_path = full_report_path.replace(".xlsx", ".pdf")

    await send_report_from_user(
        chat_id=chat_id, full_report_path=full_stat_path
    )


async def test():
    chat_id = 373084462

    now = datetime.now()

    current_week: str = await get_week_message(current_date=now)
    current_year: str = await get_year_message(current_date=now)

    act_date_period = await db_get_period_for_current_week(current_week, current_year)
    pprint(f"{act_date_period = }")

    await create_and_send_stat(chat_id, act_date_period)


if __name__ == "__main__":
    asyncio.run(test())
