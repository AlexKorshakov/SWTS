import openpyxl
from apps.core.bot.messages.messages import Messages
from apps.core.utils.generate_report.create_xlsx.get_workbook import get_workbook
from apps.core.utils.generate_report.create_xlsx.get_worksheet import get_worksheet
from apps.MyBot import bot_send_message
from loader import logger


async def create_xlsx(chat_id: int, full_act_path: str):
    """
    """

    is_created: bool = await create_new_xlsx(report_file=full_act_path)
    if is_created is None:
        logger.warning(Messages.Error.workbook_not_create)
        await bot_send_message(chat_id=chat_id, text=Messages.Error.workbook_not_create)
        return

    workbook = await get_workbook(fill_report_path=full_act_path)
    if workbook is None:
        logger.warning(Messages.Error.workbook_not_found)
        await bot_send_message(chat_id=chat_id, text=Messages.Error.workbook_not_found)
        return

    worksheet = await get_worksheet(workbook, index=0)
    if worksheet is None:
        logger.warning(Messages.Error.worksheet_not_found)
        await bot_send_message(chat_id=chat_id, text=Messages.Error.worksheet_not_found)
        return

    return workbook, worksheet


async def create_new_xlsx(report_file: str) -> bool:
    """Создание xlsx
    """
    try:
        wb = openpyxl.Workbook()
        wb.save(report_file)
        return True
    except Exception as err:
        logger.error(F"set_border {repr(err)}")
        return False
