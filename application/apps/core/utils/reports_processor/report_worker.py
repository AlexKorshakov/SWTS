import asyncio
from datetime import datetime

from pprint import pprint

from pandas import DataFrame

from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.messages.messages import Messages
from apps.core.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.utils.generate_report.generator_report import create_report_from_other_method, create_mip_report, \
    get_act_number_on_data_base, create_act_prescription, set_act_data_on_data_base
from apps.core.utils.generate_report.get_data_report import get_data_report
from apps.core.utils.generate_report.get_file_list import get_json_file_list
from apps.core.utils.generate_report.get_report_path import get_full_report_name, get_full_mip_report_name, \
    get_and_create_full_act_prescription_name
from apps.core.utils.generate_report.send_report_from_user import send_report_from_user

from apps.core.utils.reports_processor.report_worker_utils import get_clear_list_value, get_general_constractor_list, \
    get_general_constractor_data, get_clean_headers, create_lite_dataframe_from_query, get_query, format_data_db
from apps.core.utils.data_recording_processor.set_user_report_data import set_report_data, set_act_data_on_google_drive
from loader import logger


async def create_and_send_report(chat_id):
    """Формирование и отправка отчета

    :param chat_id:
    :return:
    """

    file_list = await get_json_file_list(chat_id=chat_id)
    if not file_list:
        logger.warning(Messages.Error.file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

    report_dataframe = await get_data_report(chat_id=chat_id, file_list=file_list)
    if report_dataframe.empty:
        logger.warning(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)

    full_report_path = await get_full_report_name(chat_id=chat_id)
    await create_report_from_other_method(chat_id=chat_id,
                                          dataframe=report_dataframe,
                                          full_report_path=full_report_path,
                                          file_list=file_list)

    await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    await set_report_data(chat_id=chat_id, full_report_path=full_report_path)

    await send_report_from_user(chat_id=chat_id, full_report_path=full_report_path)

    return True


async def create_and_send_mip_report(chat_id) -> bool:
    """Формирование и отправка отчета

    :param chat_id:
    :return:
    """

    full_mip_report_path: str = await get_full_mip_report_name(chat_id=chat_id)

    file_list = await get_json_file_list(chat_id=chat_id)
    if not file_list:
        logger.error(Messages.Error.file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return False

    dataframe = await get_data_report(chat_id=chat_id, file_list=file_list)
    if dataframe.empty:
        logger.error(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return False

    await create_mip_report(chat_id=chat_id,
                            dataframe=dataframe,
                            full_mip_report_path=full_mip_report_path,
                            violation_data=file_list
                            )

    await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    await set_report_data(chat_id=chat_id, full_report_path=full_mip_report_path)

    await send_report_from_user(chat_id=chat_id, full_report_path=full_mip_report_path)

    full_mip_report_path = full_mip_report_path.replace(".xlsx", ".pdf")

    await send_report_from_user(chat_id=chat_id, full_report_path=full_mip_report_path)

    return True


async def create_and_send_act_prescription(chat_id: int, query_act_date_period=None, **kwargs) -> bool:
    """Формирование актов - предписаний

    :param query_act_date_period: list период (даты) для выборки
    :param chat_id: id  пользователя
    :return:
    """

    act_date: str = datetime.now().strftime("%d.%m.%Y")  # '28.10.2022'  #

    if not query_act_date_period:
        query_act_date_period = await format_data_db(act_date)

    table_name: str = 'core_violations'
    clean_headers: list = await get_clean_headers(table_name=table_name)

    query: str = await get_query(type_query='query_act', table_name=table_name,
                                 query_act_date=query_act_date_period, user_id=chat_id)

    clear_list_value: list = await get_clear_list_value(chat_id=chat_id,
                                                        query=query,
                                                        clean_headers=clean_headers)
    if not clear_list_value:
        return False

    general_constractor_ids_list: list = await get_general_constractor_list(clear_list_value=clear_list_value)

    if not general_constractor_ids_list:
        return False

    for g_constractor_id in general_constractor_ids_list:

        query: str = await get_query(type_query='general_contractor_id', table_name=table_name,
                                     query_act_date=query_act_date_period, value_id=g_constractor_id,
                                     user_id=chat_id)

        act_dataframe: DataFrame = await create_lite_dataframe_from_query(chat_id=chat_id,
                                                                          query=query,
                                                                          clean_headers=clean_headers)
        if act_dataframe.empty:
            continue

        general_contractor: dict = await get_general_constractor_data(constractor_id=g_constractor_id,
                                                                      type_constractor='general')

        act_number: int = await get_act_number_on_data_base()
        param: dict = {
            'act_number': act_number,
            'act_date': act_date,
            'general_contractor': general_contractor.get('title'),
            'short_title': general_contractor.get('short_title'),
        }
        full_act_prescription_path: str = await get_and_create_full_act_prescription_name(chat_id=chat_id, param=param)

        act_is_created: bool = await create_act_prescription(
            chat_id=chat_id,
            act_number=act_number,
            dataframe=act_dataframe,
            full_act_path=full_act_prescription_path,
            act_date=act_date
        )

        if not act_is_created: continue

        await set_act_data_on_data_base(act_data=act_dataframe, act_num=act_number, act_date=act_date)

        await convert_report_to_pdf(chat_id=chat_id, path=full_act_prescription_path)
        await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')
        await set_act_data_on_google_drive(chat_id=chat_id, full_report_path=full_act_prescription_path)
        await send_report_from_user(chat_id=chat_id, full_report_path=full_act_prescription_path)
        full_act_prescription_path = full_act_prescription_path.replace(".xlsx", ".pdf")
        await send_report_from_user(chat_id=chat_id, full_report_path=full_act_prescription_path)

    return True


async def test():
    general_constractor = DataBase().get_dict_data_from_table_from_id(
        table_name='core_generalcontractor',
        id=2)

    pprint(general_constractor)
    return general_constractor


if __name__ == '__main__':
    chat_id = 862629360

    if '2022-10-30' == datetime.now().strftime("%Y-%m-%d"):
        print(f'data is true')

    asyncio.run(create_and_send_act_prescription(
        chat_id=chat_id,
        query_act_date_period='2022-12-01'
    ))
    # asyncio.run(test())
