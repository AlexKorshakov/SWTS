from openpyxl.styles import Border, Side

from loader import logger


async def set_act_range_border(worksheet, cell_range, border=None):
    """Форматирование ячейки: все границы ячейки

    """

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    if border:
        thin_border = Border(bottom=Side(style='thin'))

    rows = worksheet[cell_range]
    for row in rows:
        for cell in row:
            try:
                cell.border = thin_border
            except Exception as err:
                logger.error(f"set_border {repr(err)}")