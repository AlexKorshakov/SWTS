import asyncio
from datetime import datetime, timedelta
# import time
# from datetime import date
from pprint import pprint
# from time import strftime

from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.utils.generate_report.create_dataframe import create_dataframe, create_lite_dataframe
from apps.core.bot.utils.generate_report.generator_report import create_act_prescription, \
    create_report_from_other_method, create_mip_report
from loader import logger

from apps.core.bot.messages.messages import Messages
# from apps.core.bot.utils.generate_report.generator_report import create_report_from_other_method, create_mip_report, \
#     create_act_prescription
from apps.core.bot.utils.generate_report.get_data_report import get_data_report
from apps.core.bot.utils.generate_report.get_file_list import get_json_file_list
from apps.core.bot.utils.generate_report.get_report_path import get_full_report_name, get_full_mip_report_name, \
    get_full_act_prescription_name
from apps.core.bot.utils.generate_report.send_report_from_user import send_report_from_user
from apps.core.bot.utils.set_user_report_data import set_report_data, set_act_data_on_google_drive


async def create_and_send_report(chat_id):
    """Формирование и отправка отчета

    :param chat_id:
    :return:
    """

    file_list = await get_json_file_list(chat_id=chat_id)
    if not file_list:
        logger.warning(Messages.Error.file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

    dataframe = await get_data_report(chat_id=chat_id, file_list=file_list)
    if dataframe.empty:
        logger.warning(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)

    full_report_path = await get_full_report_name(chat_id=chat_id)
    await create_report_from_other_method(chat_id=chat_id,
                                          dataframe=dataframe,
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


async def create_and_send_act_prescription(chat_id: int) -> bool:
    """Формирование актов - предписаний

    :param chat_id:
    :return:
    """
    table_name = 'core_violations'
    act_date = datetime.now().strftime("%d.%m.%Y")

    headers = DataBase().get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    query: str = f'SELECT * ' \
                 f'FROM {table_name} ' \
                 f'WHERE `user_id` = {chat_id} ' \
                 f'AND `act_number` IS NULL '

    datas_query: list = DataBase().get_data_list(query=query)

    clear_list_value: list = []
    for items_value in datas_query:
        item_dict: dict = dict((header, item_value) for header, item_value in zip(clean_headers, items_value))
        clear_list_value.append(item_dict)

    general_constractor_list = [item_value.get('general_contractor_id') for item_value in clear_list_value]
    general_constractor_list = list(set(general_constractor_list))

    for g_constractor in general_constractor_list:

        # table_name = 'core_violations'
        # query: str = f'SELECT * ' \
        #              f'FROM {table_name} ' \
        #              f'WHERE `user_id` = {chat_id} ' \
        #              f'AND `general_contractor_id` = {g_constractor} ' \
        #              f'AND `act_number` IS NULL '
        #
        # datas_query: list = DataBase().get_data_list(query=query)

        general_contractor = DataBase().get_dict_data_from_table_from_id(
            table_name='core_generalcontractor',
            id=g_constractor)

        query: str = f'SELECT * ' \
                     f'FROM {table_name} ' \
                     f'WHERE `user_id` = {chat_id} ' \
                     f'AND `general_contractor_id` = {g_constractor} ' \
                     f'AND `act_number` IS NULL '

        item_datas_query: list = DataBase().get_data_list(query=query)

        dataframe = await create_lite_dataframe(data_list=item_datas_query, header_list=clean_headers)
        if dataframe.empty:
            logger.error(Messages.Error.dataframe_not_found)
            await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
            continue

        # for item in list(set(dataframe.main_location_id)):
        #     main_location = DataBase().get_dict_data_from_table_from_id(
        #         table_name='core_mainlocation',
        #         id=item)
        #
        param: dict = {
            'act_number': 70022,
            'act_date': act_date,
            'general_contractor': general_contractor.get('title'),
            'short_title': general_contractor.get('short_title'),
            # 'main_location': main_location.get('short_title')

        }
        full_act_prescription_path: str = await get_full_act_prescription_name(chat_id=chat_id, param=param)

        await create_act_prescription(
            chat_id=chat_id,
            dataframe=dataframe,
            full_act_path=full_act_prescription_path,
            act_date=act_date,
            general_contractor=general_contractor
        )

        # await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

        # await set_act_data_on_google_drive(chat_id=chat_id, full_report_path=full_act_prescription_path)

        # await send_report_from_user(chat_id=chat_id, full_report_path=full_act_prescription_path)
        #
        # full_act_prescription_path = full_act_prescription_path.replace(".xlsx", ".pdf")
        #
        # await send_report_from_user(chat_id=chat_id, full_report_path=full_act_prescription_path)
        break
    return True


async def test():
    general_constractor = DataBase().get_dict_data_from_table_from_id(
        table_name='core_generalcontractor',
        id=2)

    pprint(general_constractor)
    return general_constractor


if __name__ == '__main__':
    chat_id = 373084462
    asyncio.run(create_and_send_act_prescription(chat_id=chat_id))
    # asyncio.run(test())
