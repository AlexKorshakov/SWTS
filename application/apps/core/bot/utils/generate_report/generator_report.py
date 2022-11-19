import asyncio
from pprint import pprint

from pandas import DataFrame

from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.utils.generate_report.sheet_formatting.set_act_basic_value import set_act_body_values, \
    set_act_footer_values
from apps.core.bot.utils.generate_report.sheet_formatting.set_akt_value import set_act_header_values, \
    get_act_headlines_data_values, set_act_footer_footer_values
from apps.core.bot.utils.generate_report.sheet_formatting.set_page_setup import set_act_page_after_footer_setup
from config.web.settings import MEDIA_ROOT
from loader import logger

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.bot.utils.generate_report.create_dataframe import create_dataframe
from apps.core.bot.utils.generate_report.create_xlsx import create_xlsx, create_new_xlsx
from apps.core.bot.utils.generate_report.get_file_list import get_json_file_list
from apps.core.bot.utils.generate_report.get_report_path import get_full_report_name
from apps.core.bot.utils.generate_report.get_workbook import get_workbook
from apps.core.bot.utils.generate_report.get_worksheet import get_worksheet
from apps.core.bot.utils.generate_report.sheet_formatting.set_value import \
    set_report_header_values, \
    set_report_violation_values, set_photographic_materials_values, set_photographic_materials, \
    set_headlines_data_values, set_report_body_values, set_act_violation_values, set_act_photographic_materials_values, \
    set_act_photographic_materials
from apps.core.bot.utils.generate_report.sheet_formatting.sheet_formatting import format_sheets, \
    format_mip_report_sheet, \
    format_mip_photographic, format_act_prescription_sheet, format_act_footer_prescription_sheet, \
    format_act_photo_header, format_act_photo_description
from apps.core.bot.utils.img_processor.insert_img import insert_images_to_sheet, insert_signalline_to_report_body, \
    insert_service_image


async def create_report_from_other_method(chat_id, dataframe=None, full_report_path=None,
                                          file_list=None):
    """Создание отчета xls из данных json
    :param file_list:
    :param full_report_path:
    :param dataframe:
    :type chat_id: int
    :param chat_id:
    :return:
    """

    if full_report_path is None:
        full_report_path = await get_full_report_name(chat_id=chat_id)

    is_created: bool = await create_xlsx(dataframe, report_file=full_report_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(full_report_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    await format_sheets(worksheet)

    if not file_list:
        file_list = await get_json_file_list(chat_id=chat_id)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(full_report_path)


async def create_report(chat_id):
    """Создание отчета xls из данных json
    """

    fill_report_path = await get_full_report_name(chat_id=chat_id)
    if fill_report_path is None:
        logger.warning('error! fill_report_path not found!')
        MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        return

    file_list = await get_json_file_list(chat_id=chat_id)
    if file_list is None:
        logger.warning('error! file_list not found!')
        MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return

    dataframe = await create_dataframe(file_list=file_list)
    if dataframe is None:
        logger.warning('error! dataframe not found!')
        MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return

    is_created: bool = await create_xlsx(dataframe, report_file=fill_report_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    await format_sheets(worksheet)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(fill_report_path)

    await convert_report_to_pdf(chat_id=chat_id, path=fill_report_path)


async def create_mip_report(chat_id, dataframe=None, full_mip_report_path=None, violation_data=None):
    """Создание отчета xls из данных json


    """

    if not full_mip_report_path:
        logger.warning(Messages.Error.fill_report_path_not_found)
        return

    is_created: bool = await create_new_xlsx(report_file=full_mip_report_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path=full_mip_report_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    await format_mip_report_sheet(worksheet)

    await set_report_body_values(worksheet)

    await set_headlines_data_values(chat_id=chat_id)

    await set_report_header_values(worksheet, dataframe)

    try:
        await set_report_violation_values(worksheet, dataframe)
    except Exception:
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_not_found)
        return

    await insert_signalline_to_report_body(worksheet)

    if violation_data is None:
        violation_data = await get_json_file_list(chat_id=chat_id)

    if violation_data:
        await set_photographic_materials_values(worksheet)

        await format_mip_photographic(worksheet)

        num_data: int = 0
        for v_data in violation_data:
            is_add = await set_photographic_materials(worksheet, v_data, num_data)
            if is_add:
                num_data += 1

    workbook.save(full_mip_report_path)

    await convert_report_to_pdf(chat_id=chat_id, path=full_mip_report_path)


async def create_xlsx(chat_id: int, full_act_path: str):
    """
    """

    is_created: bool = await create_new_xlsx(report_file=full_act_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path=full_act_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    return workbook, worksheet


async def anchor_photo(dataframe, row_number, workbook, worksheet, full_act_path, act_date=None):
    """Вставка фото в ячейку с учетом смещения. Возвращает область печати с учетом фото

    """
    photo_row: int = 63 + row_number
    row_num: int = 0
    img_params: dict = {"height": 220,
                        "anchor": True,
                        "scale": True, }

    row_act_header: int = photo_row - 1
    row_act_photo: int = photo_row
    img_params["row_header"] = row_act_header
    img_params["row_description"] = row_act_photo
    img_params["row"] = row_act_photo

    for num_data, violation_data in enumerate(dataframe.itertuples(index=False), start=1):
        # TODO  проверить путь фото
        img_params["photo_full_name"] = MEDIA_ROOT + violation_data[27]

        if num_data % 2 != 0:
            img_params["column"] = 'B'
            img_params["column_img"] = 2
            img_params["column_description"] = 6
            img_params["description"] = violation_data[18]

            if num_data != 1:
                img_params["row_header"] = img_params["row_header"] + 2
                img_params["row_description"] = img_params["row_description"] + 2
                img_params["row"] = img_params["row"] + 2
                await format_act_photo_header(worksheet, img_params["row_header"])
                await format_act_photo_description(worksheet, img_params["row_description"])
                workbook.save(full_act_path)
                photo_row += 2
        else:
            img_params["column"] = 'H'
            img_params["column_img"] = 8
            img_params["column_description"] = 12
            img_params["description"] = violation_data[18]

        is_anchor: bool = False
        try:
            is_anchor = await set_act_photographic_materials(worksheet, img_params)
        except Exception as err:
            logger.error(f"set_act_photographic_materials {num_data= } {row_num=} {repr(err)} ")

        if is_anchor:
            workbook.save(full_act_path)
            # set header
            worksheet.cell(row=img_params["row_header"],
                           column=img_params["column_img"],
                           value=f'Фото {num_data}')
            workbook.save(full_act_path)

            # set description
            worksheet.cell(row=img_params["row_description"],
                           column=img_params["column_description"],
                           value=img_params["description"])
            workbook.save(full_act_path)

    print_area = f'$A$1:M{photo_row + row_num + 1}'

    return print_area


async def create_act_prescription(chat_id, act_number, dataframe, full_act_path, act_date=None) -> bool:
    """Формирование Акта-предписания из dataframe

    :param act_number:
    :param act_date:
    :param full_act_path:
    :param chat_id:
    :param dataframe: DataFrame
    """

    if not full_act_path:
        logger.warning(Messages.Error.fill_report_path_not_found)
        return False

    workbook, worksheet = await create_xlsx(chat_id, full_act_path)
    if not worksheet:
        return False

    await format_act_prescription_sheet(worksheet)

    await set_act_body_values(worksheet)

    param_insert_service_image: dict = {
        'photo_full_name': MEDIA_ROOT + "\\" + "Logo.jpg",
        "height": 75,
        "width": 230,
        "anchor": True,
        "column": 'B',
        "column_img": 2,
        "row": 2,
    }

    await insert_service_image(worksheet, param_insert_service_image)

    headlines_data_values: dict = await get_act_headlines_data_values(
        chat_id=chat_id, dataframe=dataframe, act_date=act_date, act_number=act_number
    )
    await set_act_header_values(worksheet, headlines_data=headlines_data_values)
    workbook.save(full_act_path)

    try:
        row_number = await set_act_violation_values(worksheet, dataframe, workbook, full_act_path)
    except Exception as err:
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_not_found + str(f' {err} '))
        logger.error(f'create_act_prescription: set_act_violation_values error: {repr(err)}')
        return False

    await format_act_footer_prescription_sheet(worksheet, row_number)
    await set_act_footer_values(worksheet, row_number)
    await set_act_footer_footer_values(worksheet, row_number)

    await set_act_photographic_materials_values(worksheet, row_number)
    # await format_act_photographic(worksheet, row_number)
    await format_act_photo_header(worksheet, row_number=62 + row_number)
    await format_act_photo_description(worksheet, row_number=63 + row_number)

    workbook.save(full_act_path)

    print_area = await anchor_photo(dataframe=dataframe, row_number=row_number,
                                    workbook=workbook, worksheet=worksheet,
                                    full_act_path=full_act_path, act_date=act_date)

    await set_act_page_after_footer_setup(worksheet, print_area)

    workbook.save(full_act_path)

    return True


async def get_act_number_on_data_base() -> int:
    """Получение номера акта из Database `core_reestreacts`

    :return: int act_num: номер акта - предписания
    """
    act_num: int = DataBase().get_max_max_number() + 1
    return act_num


async def set_act_data_on_data_base(act_data: DataFrame, act_num: int, act_date: str) -> None:
    """Запись данных в Database `core_reestreacts` и дополнение данных в `core_violations` ели был оформлен акт

    :return:
    """
    act_is_created: bool = DataBase().set_act_value(act_data,
                                                    act_number=act_num,
                                                    act_date=act_date)
    if not act_is_created:
        return

    for act_id in act_data.id:
        DataBase().update_column_value(column_name='act_number', value=str(act_num), id=act_id)


if __name__ == '__main__':
    asyncio.run(get_act_number_on_data_base())
