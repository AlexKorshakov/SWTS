from loader import logger


async def set_merge_cells(worksheet, merged_cell):
    """ФОрматирование: jбьединение ячеек

    :param worksheet:
    :param merged_cell:
    :return:
    """
    try:
        worksheet.merge_cells(merged_cell)
    except Exception as err:
        logger.error(f"set_merge_cells {repr(err)}")
