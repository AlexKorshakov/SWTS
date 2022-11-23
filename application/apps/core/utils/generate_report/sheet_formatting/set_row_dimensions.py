from loader import logger


async def set_row_dimensions(worksheet, row_number, height):
    try:
        worksheet.row_dimensions[int(row_number)].height = float(height)
    except Exception as err:
        logger.error(f"set_row_dimensions {repr(err)}")
