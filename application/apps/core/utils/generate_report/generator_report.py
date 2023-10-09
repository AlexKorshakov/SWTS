import asyncio
import os

from pandas import DataFrame

from apps.MyBot import bot_send_message
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import (db_get_max_max_number,
                                         db_set_act_value,
                                         db_update_column_value)
from apps.core.utils.generate_report.convert_xlsx_to_pdf import \
    convert_report_to_pdf
from apps.core.utils.generate_report.create_dataframe import create_dataframe
from apps.core.utils.generate_report.create_xlsx.create_xlsx import create_xlsx
from apps.core.utils.generate_report.generate_act_prescription.set_act_format_ import (
    format_act_photo_description, format_act_photo_header)
from apps.core.utils.generate_report.generate_act_prescription.set_act_value import \
    get_act_headlines_data_values
from apps.core.utils.generate_report.generate_act_prescription.set_act_values import \
    set_act_photographic_materials
from apps.core.utils.secondary_functions.get_filepath import get_photo_full_name
from apps.core.utils.generate_report.get_file_list import get_json_file_list
from apps.core.utils.generate_report.get_report_path import \
    get_full_report_name
from apps.core.utils.generate_report.sheet_formatting.sheet_formatting import \
    format_sheets
from apps.core.utils.img_processor.insert_img import insert_images_to_sheet
from apps.core.utils.reports_processor.report_worker_utils import \
    get_clean_headers
from config.config import Udocan_media_path
from loader import logger


async def create_report_from_other_method(chat_id, full_report_path=None,
                                          file_list=None):
    """Создание отчета xls из данных json
    :param file_list:
    :param full_report_path:
    :type chat_id: int
    :param chat_id:
    :return:
    """

    if full_report_path is None:
        full_report_path = await get_full_report_name(chat_id=chat_id)

    workbook, worksheet = await create_xlsx(chat_id, full_report_path)
    if not worksheet:
        return False

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
        await bot_send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        return

    file_list = await get_json_file_list(chat_id=chat_id)
    if file_list is None:
        logger.warning('error! file_list not found!')
        await bot_send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return

    dataframe = await create_dataframe(file_list=file_list)
    if dataframe is None:
        logger.warning('error! dataframe not found!')
        await bot_send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return

    workbook, worksheet = await create_xlsx(chat_id, fill_report_path)
    if not worksheet:
        return False

    await format_sheets(worksheet)

    await insert_images_to_sheet(file_list, worksheet)

    workbook.save(fill_report_path)

    await convert_report_to_pdf(chat_id=chat_id, path=fill_report_path)


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

    table_name: str = 'core_violations'
    clean_headers: list = await get_clean_headers(table_name=table_name)

    for num_data, violation_data in enumerate(dataframe.itertuples(index=False), start=1):
        # for num_data, violation_data in enumerate(df.to_dict('index'), start=1):

        violation_dict = dict(zip(clean_headers, violation_data))

        # img_params["photo_full_name"] = str (Udocan_media_path) + os.sep + str(violation_dict.get('photo', None))
        img_params["photo_full_name"] = await get_photo_full_name(
            media_path=str(Udocan_media_path),
            photo_path=str(violation_dict.get('photo', None))
        )

        if num_data % 2 != 0:
            img_params["column"] = 'B'
            img_params["column_img"] = 2
            img_params["column_description"] = 6
            img_params["description"] = violation_dict.get('description', None)

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
            img_params["description"] = violation_dict.get('description', None)

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


async def get_act_number_on_data_base() -> int:
    """Получение номера акта из Database `core_reestreacts`

    :return: int act_num: номер акта - предписания
    """
    act_num: int = await db_get_max_max_number() + 1
    return act_num


async def set_act_data_on_data_base(act_data: DataFrame, act_num: int, act_date: str) -> None:
    """Запись данных в Database `core_reestreacts` и дополнение данных в `core_violations` ели был оформлен акт

    :return:
    """
    act_is_created: bool = await db_set_act_value(act_data,
                                                  act_number=act_num,
                                                  act_date=act_date)
    if not act_is_created:
        return

    for act_id in act_data.id:
        await db_update_column_value(column_name='act_number', value=str(act_num), violation_id=act_id)


async def test():
    chat_id = 373084462
    await get_act_headlines_data_values(chat_id)


if __name__ == "__main__":
    asyncio.run(test())
