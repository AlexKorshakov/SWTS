from apps.core.bot.utils.generate_report.settings_act_prescription import ACT_RANGE_COLUMNS, ACT_MERGED_CELLS, \
    ACT_CELL_RANGES, ACT_ROW_DIMENSIONS, ACT_CELL_RANGES_BASIC_ALIGNMENT, ACT_CELL_RANGES_SET_REPORT_FONT
from loader import logger
from xlsxwriter.worksheet import Worksheet

from apps.core.bot.utils.generate_report.settings_mip_report import RANGE_COLUMNS, MERGED_CELLS, ROW_DIMENSIONS, \
    CELL_RANGE_BACKGROUND_COLOR, CELL_RANGES_ALIGNMENT, CELL_RANGES_BASIC_ALIGNMENT, \
    CELL_RANGES_SET_REPORT_FONT, CELL_RANGES
from apps.core.bot.utils.generate_report.sheet_formatting.set_alignment import set_alignment, set_mip_alignment, \
    set_act_alignment
from apps.core.bot.utils.generate_report.sheet_formatting.set_background_color import set_background_color
from apps.core.bot.utils.generate_report.sheet_formatting.set_column_widths import set_column_widths
from apps.core.bot.utils.generate_report.sheet_formatting.set_font import set_font, set_report_font, sets_report_font
from apps.core.bot.utils.generate_report.sheet_formatting.set_frame_border import set_border, set_range_border, \
    set_act_range_border
from apps.core.bot.utils.generate_report.sheet_formatting.set_page_setup import set_page_setup, set_act_page_setup
from apps.core.bot.utils.generate_report.sheet_formatting.set_row_height import set_row_height


async def format_sheets(worksheet: Worksheet):
    """Пошаговое форматирование страницы
    """

    await set_border(worksheet)
    await set_alignment(worksheet)
    await set_font(worksheet)
    await set_column_widths(worksheet)
    await set_row_height(worksheet)


async def format_mip_report_sheet(worksheet: Worksheet):
    """Пошаговое форматирование страницы
    """

    for item in RANGE_COLUMNS:

        try:
            worksheet.column_dimensions[item[0]].width = item[1]
        except Exception as err:
            logger.error(f"set_column_widths {repr(err)}")

    await set_page_setup(worksheet)

    for merged_cell in MERGED_CELLS:
        worksheet.merge_cells(merged_cell)

    await set_range_border(worksheet, cell_range=CELL_RANGES)

    for item in ROW_DIMENSIONS:
        worksheet.row_dimensions[int(item[0])].height = float(item[1])

    for item, cell_range in enumerate(CELL_RANGES_BASIC_ALIGNMENT, start=1):
        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    for item in CELL_RANGE_BACKGROUND_COLOR:
        await set_background_color(worksheet, item[0], rgb=item[1])

    for item, cell_range in enumerate(CELL_RANGES_BASIC_ALIGNMENT, start=1):
        await set_mip_alignment(worksheet, cell_range, horizontal='left', vertical='center')

    for item, cell_range in enumerate(CELL_RANGES_ALIGNMENT, start=1):
        await set_mip_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    for item, cell_range in enumerate(CELL_RANGES_SET_REPORT_FONT, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])


async def format_act_prescription_sheet(worksheet: Worksheet):
    """Пошаговое форматирование страницы
    """

    for item in ACT_RANGE_COLUMNS:
        try:
            worksheet.column_dimensions[item[0]].width = item[1]
        except Exception as err:
            logger.error(f"set_column_widths {repr(err)}")

    await set_act_page_setup(worksheet)

    for merged_cell in ACT_MERGED_CELLS:
        worksheet.merge_cells(merged_cell)

    for item in ACT_CELL_RANGES:
        await set_act_range_border(worksheet, cell_range=item[0], border=item[1])

    for item in ACT_ROW_DIMENSIONS:
        worksheet.row_dimensions[int(item[0])].height = float(item[1])

    for num, item_range in enumerate(ACT_CELL_RANGES_BASIC_ALIGNMENT, start=1):
        await set_report_font(worksheet, cell_range=item_range[0], font_size=item_range[2], font_name=item_range[1])

    # for item in CELL_RANGE_BACKGROUND_COLOR:
    #     await set_background_color(worksheet, item[0], rgb=item[1])

    for item, item_range in enumerate(ACT_CELL_RANGES_BASIC_ALIGNMENT, start=1):
        await set_act_alignment(worksheet, item_range[0], horizontal=item_range[3], vertical=item_range[4])

    # for item, cell_range in enumerate(CELL_RANGES_ALIGNMENT, start=1):
    #     await set_mip_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    for item, cell_range in enumerate(ACT_CELL_RANGES_SET_REPORT_FONT, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])


async def format_mip_photographic(worksheet):
    """

    :return:
    """
    merged_cells = [
        'C50:H50',
        'C51:E51',
        'G51:H51',
    ]

    for merged_cell in merged_cells:
        worksheet.merge_cells(merged_cell)

    photographic_materials_alignment = [
        'C50:H50',
        'C51:H51',
    ]

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_mip_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_range_border(worksheet, cell_range=cell_range)

    photographic_row_dimensions = [
        ["50", "35.0"],
        ["51", "35.0"],
    ]

    for item in photographic_row_dimensions:
        worksheet.row_dimensions[int(item[0])].height = float(item[1])

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    photographic_report_font = [
        ['C50:H50', {"font_size": "16", "bold": "True", "name": "Arial"}],
        ['C51:H51', {"font_size": "14", "bold": "True", "name": "Arial"}]
    ]

    for item, cell_range in enumerate(photographic_report_font, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])

    background_color = [
        ["C50:H50", "FFFFC000"]
    ]

    for item in background_color:
        await set_background_color(worksheet, item[0], rgb=item[1])
