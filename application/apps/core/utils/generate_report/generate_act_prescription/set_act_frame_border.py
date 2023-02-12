from loader import logger
from openpyxl.styles import Border, Side


async def set_range_border(worksheet, cell_range, border):
    """Форматирование ячейки: все границы ячейки

    border - только нижняя граница
    """

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    if border:
        thin_border = Border(bottom=Side(style='thin'))

    rows = worksheet[cell_range]

    try:
        for row in rows:
            for cell in row:
                try:
                    cell.border = thin_border
                except Exception as err:
                    logger.error(f"set_border {repr(err)}")
                    continue
    except Exception as err:
        logger.error(f"set_border {repr(err)}")
        return False
