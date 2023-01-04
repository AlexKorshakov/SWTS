from apps.MyBot import MyBot
from apps.core.bot.messages.messages import Messages
from apps.core.utils.generate_report.convert_xlsx_to_pdf import convert_report_to_pdf
from apps.core.utils.generate_report.create_xlsx.create_xlsx import create_new_xlsx
from apps.core.utils.generate_report.create_xlsx.get_workbook import get_workbook
from apps.core.utils.generate_report.create_xlsx.get_worksheet import get_worksheet
from apps.core.utils.generate_report.generate_daily_report.format_daily_report import format_mip_report_sheet, \
    format_mip_photographic
from apps.core.utils.generate_report.generate_daily_report.set_daily_report_values import set_report_body_values, \
    set_report_headlines_data_values, set_report_header_values, set_report_violation_values, \
    set_mip_photographic_materials_values
from apps.core.utils.generate_report.get_file_list import get_json_file_list
from apps.core.utils.generate_report.set_value import set_photographic_materials
from apps.core.utils.img_processor.insert_img import insert_signalline_to_report_body
from loader import logger


async def create_daily_report(chat_id, dataframe=None, full_mip_report_path=None, violation_data=None):
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

    await set_report_headlines_data_values(chat_id=chat_id)

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
        await set_mip_photographic_materials_values(worksheet)

        await format_mip_photographic(worksheet)

        num_data: int = 0
        for v_data in violation_data:
            is_add = await set_photographic_materials(worksheet, v_data, num_data)
            if is_add:
                num_data += 1

    workbook.save(full_mip_report_path)

    await convert_report_to_pdf(chat_id=chat_id, path=full_mip_report_path)