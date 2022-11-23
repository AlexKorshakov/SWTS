from loader import logger


async def set_merge_cells(worksheet, merged_cell):
    try:
        worksheet.merge_cells(merged_cell)
    except Exception as err:
        logger.error(f"set_merge_cells {repr(err)}")
