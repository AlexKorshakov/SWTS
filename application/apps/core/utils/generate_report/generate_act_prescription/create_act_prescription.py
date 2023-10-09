from pandas import DataFrame

from apps.core.bot.messages.messages import Messages
from apps.core.utils.generate_report.create_xlsx.create_xlsx import create_xlsx
from apps.core.utils.generate_report.generate_act_prescription.set_act_basic_value import (
    set_act_body_values)
from apps.core.utils.generate_report.generate_act_prescription.set_act_format_ import (
    format_act_footer_prescription_sheet, format_act_photo_description,
    format_act_photo_header, format_act_prescription_sheet)
from apps.core.utils.generate_report.generate_act_prescription.set_act_page_setup import \
    set_act_page_after_footer_setup
from apps.core.utils.generate_report.generate_act_prescription.set_act_value import (
    get_act_headlines_data_values, set_act_footer_footer_values,
    set_act_header_values, set_act_footer_values)
from apps.core.utils.generate_report.generate_act_prescription.set_act_values import (
    set_act_photographic_materials_values, set_act_violation_values)
from apps.core.utils.generate_report.generator_report import anchor_photo
from apps.core.utils.img_processor.insert_img import insert_service_image
from apps.MyBot import bot_send_message
from apps.core.utils.secondary_functions.get_filepath import get_image_name
from loader import logger


async def create_act_prescription(chat_id: int, act_number: int, dataframe: DataFrame, full_act_path: str,
                                  act_date: str = None, qr_img_insert: bool = False) -> bool:
    """Формирование Акта-предписания из dataframe

    :param qr_img_insert:
    :param act_number: int
    :param act_date:
    :param full_act_path:
    :param chat_id: int
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

    await insert_service_image(worksheet, chat_id=chat_id, service_image_name=f'company_{chat_id}')

    if qr_img_insert:
        qr_img_params: dict = {
            "height": 150,
            "width": 150,
            "anchor": True,
            "column": 'K',
            "column_img": 11,
            "row": 1,
        }
        service_image_name: str = await get_image_name(
            str(chat_id), 'data_file', act_date, 'reports', f'qr_act_nom_{chat_id}_{act_number}'
        )

        await insert_service_image(worksheet,
                                   service_image_name=service_image_name,
                                   img_params=qr_img_params)

    headlines_data_values: dict = await get_act_headlines_data_values(
        chat_id=chat_id, dataframe=dataframe, act_date=act_date, act_number=act_number
    )
    await set_act_header_values(worksheet, headlines_data=headlines_data_values)
    workbook.save(full_act_path)

    try:
        row_number = await set_act_violation_values(worksheet, dataframe, workbook, full_act_path)

    except Exception as err:
        await bot_send_message(chat_id=chat_id, text=f'Messages.Error.file_not_found {repr(err)} ')
        logger.error(f'create_act_prescription: set_act_violation_values error: {repr(err)}')
        return False

    await format_act_footer_prescription_sheet(worksheet, row_number)
    await set_act_footer_values(worksheet, row_number)
    await set_act_footer_footer_values(worksheet, row_number)

    workbook.save(full_act_path)
    img_params: dict = {
        "height": 62,
        "width": 130,
        "anchor": True,
        "column": 'H',
        "column_img": 8,
        "row": 42 + row_number,
    }

    await insert_service_image(worksheet, chat_id=chat_id, service_image_name=f'signature_{chat_id}',
                               img_params=img_params)

    await set_act_photographic_materials_values(worksheet, row_number)
    # await format_act_photographic(worksheet, row_number)
    await format_act_photo_header(worksheet, row_number=62 + row_number)
    await format_act_photo_description(worksheet, row_number=63 + row_number)

    workbook.save(full_act_path)

    print_area: str = await anchor_photo(dataframe=dataframe, row_number=row_number,
                                         workbook=workbook, worksheet=worksheet,
                                         full_act_path=full_act_path, act_date=act_date)

    await set_act_page_after_footer_setup(worksheet, print_area)

    workbook.save(full_act_path)

    #  headlines_data = {}

    return True
