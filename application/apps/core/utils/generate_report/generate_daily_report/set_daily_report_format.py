# from apps.core.utils.generate_report.generate_act_prescription.set_act_alignment import set_act_alignment
# from apps.core.utils.generate_report.generate_act_prescription.set_act_frame_border import set_range_border
from apps.core.utils.generate_report.generate_daily_report.set_daily_report_alignment import \
    set_report_alignment
from apps.core.utils.generate_report.generate_daily_report.settings_mip_report import (
    D_REPORT_CELL_RANGE_BACKGROUND_COLOR_HEADER,
    D_REPORT_CELL_RANGES_ALIGNMENT_HEADER,
    D_REPORT_CELL_RANGES_BASIC_ALIGNMENT, D_REPORT_CELL_RANGES_HEADER,
    D_REPORT_CELL_RANGES_SET_REPORT_FONT_HEADER, D_REPORT_MERGED_CELLS_HEADER,
    D_REPORT_RANGE_COLUMNS_BASIC, D_REPORT_ROW_DIMENSIONS_HEADER)
from apps.core.utils.generate_report.sheet_formatting.set_background_color import \
    set_report_background_color
from apps.core.utils.generate_report.sheet_formatting.set_column_dimensions import \
    set_column_dimensions
from apps.core.utils.generate_report.sheet_formatting.set_font import (
    set_report_font, sets_report_font)
from apps.core.utils.generate_report.sheet_formatting.set_frame_border import \
    set_range_border
from apps.core.utils.generate_report.sheet_formatting.set_merge_cells import \
    set_merge_cells
from apps.core.utils.generate_report.sheet_formatting.set_page_setup import \
    set_page_setup
from apps.core.utils.generate_report.sheet_formatting.set_row_dimensions import \
    set_row_dimensions
from xlsxwriter.worksheet import Worksheet


# async def format_daily_report_sheet(worksheet: Worksheet, workbook, full_daily_report_report_path) -> bool:
#     """Пошаговое форматирование страницы
#     """
#
#     await format_daily_report_sheet_header(worksheet)
#     # await format_daily_report_sheet_body(worksheet, workbook, full_daily_report_report_path)
#     # await format_daily_report_sheet_footer(worksheet, workbook, full_daily_report_report_path)
#
#     return True


async def format_daily_report_sheet_basic(worksheet: Worksheet) -> bool:
    await set_page_setup(worksheet)

    for item in D_REPORT_RANGE_COLUMNS_BASIC:
        await set_column_dimensions(worksheet, column=item[0], width=item[1])

    for item_range in D_REPORT_CELL_RANGES_BASIC_ALIGNMENT:
        await set_report_font(worksheet, cell_range=item_range[0], font_size=item_range[2], font_name=item_range[1])

    for cell_range in D_REPORT_CELL_RANGES_BASIC_ALIGNMENT:
        await set_report_alignment(worksheet, cell_range[0], horizontal='left', vertical='center')

    return True


async def format_daily_report_sheet_header(worksheet: Worksheet) -> bool:
    """Пошаговое форматирование страницы
    """

    for merged_cell in D_REPORT_MERGED_CELLS_HEADER:
        await set_merge_cells(worksheet, merged_cell=merged_cell)

    for item in D_REPORT_CELL_RANGES_HEADER:
        await set_range_border(worksheet, cell_range=item[0], border=item[1])

    for item in D_REPORT_ROW_DIMENSIONS_HEADER:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])

    for item in D_REPORT_CELL_RANGE_BACKGROUND_COLOR_HEADER:
        await set_report_background_color(worksheet, item[0], rgb=item[1])

    for cell_range in D_REPORT_CELL_RANGES_ALIGNMENT_HEADER:
        await set_report_alignment(worksheet, cell_range[0], horizontal='center', vertical='center')

    for cell_range in D_REPORT_CELL_RANGES_SET_REPORT_FONT_HEADER:
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])

    return True


async def format_daily_report_sheet_body(worksheet: Worksheet, workbook, full_daily_report_report_path,
                                         num: int) -> bool:
    """Пошаговое форматирование страницы
    """

    D_REPORT_MERGED_CELLS_BODY = [
        f'C19:C{num}',
    ]

    for merged_cell in D_REPORT_MERGED_CELLS_BODY:
        await set_merge_cells(worksheet, merged_cell=merged_cell)
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGES_BODY = [
        (f'C19:H{num}', False),
    ]

    for item in D_REPORT_CELL_RANGES_BODY:
        await set_range_border(worksheet, cell_range=item[0], border=item[1])
    workbook.save(full_daily_report_report_path)

    D_REPORT_ROW_DIMENSIONS_BODY: list = []
    for item in range(19, num + 1):
        D_REPORT_ROW_DIMENSIONS_BODY.append([f"{item}", "33.0"])

    for item in D_REPORT_ROW_DIMENSIONS_BODY:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGE_BACKGROUND_COLOR_BODY = [
        [f"C19:C{num}", "FFDCDAFA"],
    ]
    for item in D_REPORT_CELL_RANGE_BACKGROUND_COLOR_BODY:
        await set_report_background_color(worksheet, item[0], rgb=item[1])
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGES_ALIGNMENT_BODY = [

    ]

    for cell_range in D_REPORT_CELL_RANGES_ALIGNMENT_BODY:
        await set_report_alignment(worksheet, cell_range[0], horizontal='center', vertical='center')
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGES_SET_REPORT_FONT_BODY = [

    ]

    for cell_range in D_REPORT_CELL_RANGES_SET_REPORT_FONT_BODY:
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])
    workbook.save(full_daily_report_report_path)

    return True


async def format_daily_report_sheet_footer(worksheet: Worksheet, workbook,
                                           full_daily_report_report_path, num) -> tuple[bool, int]:
    """Пошаговое форматирование страницы
    """
    D_REPORT_MERGED_CELLS_FOOTER = [
        f'C{num + 1}:H{num + 1}',
        f'C{num + 2}:H{num + 2}',
    ]

    for merged_cell in D_REPORT_MERGED_CELLS_FOOTER:
        await set_merge_cells(worksheet, merged_cell=merged_cell)
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGES_FOOTER = [
        (f'C2:H{num + 1}', False),
        (f'C2:H{num + 2}', False),
    ]

    for item in D_REPORT_CELL_RANGES_FOOTER:
        await set_range_border(worksheet, cell_range=item[0], border=item[1])
    workbook.save(full_daily_report_report_path)

    D_REPORT_ROW_DIMENSIONS_FOOTER = [
        [f"{num + 1}", "17.4"],
        [f"{num + 2}", "58.2"],
        [f"{num + 3}", "33.0"],
    ]

    for item in D_REPORT_ROW_DIMENSIONS_FOOTER:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGE_BACKGROUND_COLOR_FOOTER = [
        [f"C{num + 1}:H{num + 1}", "FFFFC000"],
    ]

    for item in D_REPORT_CELL_RANGE_BACKGROUND_COLOR_FOOTER:
        await set_report_background_color(worksheet, item[0], rgb=item[1])
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGES_ALIGNMENT_FOOTER = [
        (f"C{num + 1}:H{num + 1}", 'Times New Roman', 14, 'center', 'center'),
        (f"C{num + 2}:H{num + 2}", 'Times New Roman', 14, 'center', 'center'),
    ]

    for cell_range in D_REPORT_CELL_RANGES_ALIGNMENT_FOOTER:
        await set_report_alignment(worksheet, cell_range[0], horizontal='center', vertical='center')
    workbook.save(full_daily_report_report_path)

    D_REPORT_CELL_RANGES_SET_REPORT_FONT_FOOTER = [
        [f"C{num + 1}:H{num + 1}", {"font_size": "14", "bold": "True", "name": "Arial"}],
        [f"C{num + 2}:H{num + 2}", {"font_size": "14", "bold": "True", "name": "Arial"}],
    ]

    for cell_range in D_REPORT_CELL_RANGES_SET_REPORT_FONT_FOOTER:
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])
    workbook.save(full_daily_report_report_path)

    return True, num + 2


async def format_daily_report_photographic(worksheet, num: int = None) -> bool:
    """

    :return:
    """
    merged_cells = [
        f'C{num + 0}:H{num + 0}',
        f'C{num + 1}:E{num + 1}',
        f'G{num + 1}:H{num + 1}',
    ]
    for merged_cell in merged_cells:
        worksheet.merge_cells(merged_cell)

    photographic_materials_alignment = [
        f'C{num + 0}:H{num + 0}',
        f'C{num + 1}:H{num + 1}',
    ]
    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_report_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_range_border(worksheet, cell_range=cell_range)

    photographic_row_dimensions = [
        [f"{num + 0}", "35.0"],
        [f"{num + 1}", "35.0"],
    ]

    for item in photographic_row_dimensions:
        worksheet.row_dimensions[int(item[0])].height = float(item[1])

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    photographic_report_font = [
        [f'C{num + 0}:H{num + 0}', {"font_size": "16", "bold": "True", "name": "Arial"}],
        [f'C{num + 1}:H{num + 1}', {"font_size": "14", "bold": "True", "name": "Arial"}]
    ]

    for item, cell_range in enumerate(photographic_report_font, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])

    background_color = [
        [f"C{num + 0}:H{num + 0}", "FFFFC000"]
    ]

    for item in background_color:
        await set_report_background_color(worksheet, item[0], rgb=item[1])

    return True
