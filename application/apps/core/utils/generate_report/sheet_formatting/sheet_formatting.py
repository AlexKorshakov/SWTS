from apps.core.utils.generate_report.settings_act_prescription import ACT_RANGE_COLUMNS, ACT_MERGED_CELLS, \
    ACT_CELL_RANGES, ACT_ROW_DIMENSIONS, ACT_CELL_RANGES_BASIC_ALIGNMENT, ACT_CELL_RANGES_SET_REPORT_FONT
from apps.core.utils.generate_report.settings_mip_report import RANGE_COLUMNS, MERGED_CELLS, CELL_RANGES, \
    ROW_DIMENSIONS, CELL_RANGES_BASIC_ALIGNMENT, CELL_RANGE_BACKGROUND_COLOR, CELL_RANGES_ALIGNMENT, \
    CELL_RANGES_SET_REPORT_FONT
from apps.core.utils.generate_report.sheet_formatting.set_alignment import set_alignment, set_mip_alignment, \
    set_act_alignment
from apps.core.utils.generate_report.sheet_formatting.set_background_color import set_background_color
from apps.core.utils.generate_report.sheet_formatting.set_column_dimensions import set_column_dimensions
from apps.core.utils.generate_report.sheet_formatting.set_column_widths import set_column_widths
from apps.core.utils.generate_report.sheet_formatting.set_font import set_font, set_report_font, sets_report_font
from apps.core.utils.generate_report.sheet_formatting.set_frame_border import set_border, set_range_border, \
    set_act_range_border
from apps.core.utils.generate_report.sheet_formatting.set_merge_cells import set_merge_cells
from apps.core.utils.generate_report.sheet_formatting.set_page_setup import set_page_setup, set_act_page_setup, \
    set_act_page_after_footer_setup
from apps.core.utils.generate_report.sheet_formatting.set_row_dimensions import set_row_dimensions
from apps.core.utils.generate_report.sheet_formatting.set_row_height import set_row_height
from loader import logger
from xlsxwriter.worksheet import Worksheet


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
    await set_act_page_setup(worksheet)

    for item in ACT_RANGE_COLUMNS:
        await set_column_dimensions(worksheet, column=item[0], width=item[1])

    for merged_cell in ACT_MERGED_CELLS:
        await set_merge_cells(worksheet, merged_cell=merged_cell)

    for item in ACT_CELL_RANGES:
        await set_act_range_border(worksheet, cell_range=item[0], border=item[1])

    for item in ACT_ROW_DIMENSIONS:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])

    for item_range in ACT_CELL_RANGES_BASIC_ALIGNMENT:
        await set_report_font(worksheet, cell_range=item_range[0], font_size=item_range[2], font_name=item_range[1])

    for item_range in ACT_CELL_RANGES_BASIC_ALIGNMENT:
        await set_act_alignment(worksheet, item_range[0], horizontal=item_range[3], vertical=item_range[4])

    for cell_range in ACT_CELL_RANGES_SET_REPORT_FONT:
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])


async def format_act_footer_prescription_sheet(worksheet: Worksheet, row_number):
    """Пошаговое форматирование страницы
    """
    await set_act_page_setup(worksheet)

    ACT_FOOTER_MERGED_CELLS = [
        f'B{30 + row_number}:L{30 + row_number}', f'B{31 + row_number}:F{31 + row_number}',
        f'G{31 + row_number}:L{31 + row_number}', f'B{32 + row_number}:F{32 + row_number}',
        f'G{32 + row_number}:L{32 + row_number}', f'B{33 + row_number}:L{33 + row_number}',
        f'B{35 + row_number}:L{35 + row_number}', f'B{36 + row_number}:L{36 + row_number}',
        f'B{38 + row_number}:L{38 + row_number}', f'B{39 + row_number}:L{39 + row_number}',
        f'B{40 + row_number}:L{40 + row_number}', f'B{42 + row_number}:F{42 + row_number}',
        f'B{43 + row_number}:F{43 + row_number}', f'H{43 + row_number}:I{43 + row_number}',
        f'K{43 + row_number}:L{43 + row_number}', f'B{44 + row_number}:F{44 + row_number}',
        f'H{44 + row_number}:I{44 + row_number}', f'K{44 + row_number}:L{44 + row_number}',
        f'K{46 + row_number}:L{46 + row_number}', f'K{47 + row_number}:L{47 + row_number}',
        f'B{49 + row_number}:L{49 + row_number}', f'B{50 + row_number}:L{50 + row_number}',
        f'B{51 + row_number}:L{51 + row_number}', f'K{52 + row_number}:L{52 + row_number}',
        f'K{53 + row_number}:L{53 + row_number}', f'K{54 + row_number}:L{54 + row_number}',
        f'K{55 + row_number}:L{55 + row_number}',
    ]
    for merged_cell in ACT_FOOTER_MERGED_CELLS:
        await set_merge_cells(worksheet, merged_cell=merged_cell)

    ACT_FOOTER_CELL_RANGES = [
        (f'B{35 + row_number}:L{35 + row_number}', False),
        (f'B{36 + row_number}:L{36 + row_number}', False),
        (f'B{38 + row_number}:L{38 + row_number}', False),
        (f'B{39 + row_number}:L{39 + row_number}', False),
        (f'B{40 + row_number}:L{40 + row_number}', False),
        (f'B{43 + row_number}:F{43 + row_number}', True),
        (f'H{43 + row_number}:I{43 + row_number}', True),
        (f'K{43 + row_number}:L{43 + row_number}', True),
        (f'K{46 + row_number}:L{46 + row_number}', True),
        (f'B{50 + row_number}:L{50 + row_number}', True),
        (f'K{52 + row_number}:L{52 + row_number}', True),
        (f'K{54 + row_number}:L{54 + row_number}', True),
    ]
    for item in ACT_FOOTER_CELL_RANGES:
        await set_act_range_border(worksheet, cell_range=item[0], border=item[1])

    ACT_FOOTER_ROW_DIMENSIONS = [
        [f'{29 + row_number}', '5.5'], [f'{30 + row_number}', '45'], [f'{31 + row_number}', '18'],
        [f'{32 + row_number}', '18'], [f'{33 + row_number}', '30'], [f'{34 + row_number}', '5.5'],
        [f'{35 + row_number}', '18'], [f'{36 + row_number}', '32'], [f'{37 + row_number}', '5.5'],
        [f'{38 + row_number}', '20'], [f'{39 + row_number}', '18'], [f'{40 + row_number}', '30'],
        [f'{41 + row_number}', '18'], [f'{42 + row_number}', '18'], [f'{43 + row_number}', '30'],
        [f'{44 + row_number}', '18'], [f'{45 + row_number}', '18'], [f'{46 + row_number}', '18'],
        [f'{47 + row_number}', '18'], [f'{48 + row_number}', '18'], [f'{49 + row_number}', '18'],
        [f'{50 + row_number}', '30'], [f'{51 + row_number}', '40'], [f'{52 + row_number}', '18'],
        [f'{53 + row_number}', '18'], [f'{54 + row_number}', '18'], [f'{55 + row_number}', '18'],
    ]
    for item in ACT_FOOTER_ROW_DIMENSIONS:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])

    ACT_FOOTER_CELL_RANGES_BASIC_ALIGNMENT = [
        (f'B{30 + row_number}:L{30 + row_number}', 'Times New Roman', 11, 'center', 'center'),
        (f'B{31 + row_number}:L{31 + row_number}', 'Times New Roman', 11, 'center', 'center'),
        (f'B{32 + row_number}:L{32 + row_number}', 'Times New Roman', 11, 'center', 'center'),
        (f'B{33 + row_number}:L{33 + row_number}', 'Times New Roman', 12, 'center', 'center'),
        (f'B{35 + row_number}:L{35 + row_number}', 'Times New Roman', 14, 'left', 'center'),
        (f'B{36 + row_number}:L{36 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{38 + row_number}:L{38 + row_number}', 'Times New Roman', 12, 'center', 'center'),
        (f'B{40 + row_number}:L{40 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{42 + row_number}:L{42 + row_number}', 'Times New Roman', 14, 'center', 'center'),
        (f'B{43 + row_number}:L{43 + row_number}', 'Times New Roman', 12, 'center', 'center'),
        (f'B{44 + row_number}:L{44 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{46 + row_number}:L{46 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{47 + row_number}:L{47 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{49 + row_number}:L{49 + row_number}', 'Times New Roman', 12, 'left', 'center'),
        (f'B{51 + row_number}:L{51 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{53 + row_number}:L{53 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{55 + row_number}:L{55 + row_number}', 'Times New Roman', 10, 'center', 'center'),
        (f'B{59 + row_number}:L{59 + row_number}', 'Times New Roman', 10, 'right', 'center'),
        (f'B{60 + row_number}:L{60 + row_number}', 'Times New Roman', 10, 'right', 'center'),
    ]
    for item_range in ACT_FOOTER_CELL_RANGES_BASIC_ALIGNMENT:
        await set_report_font(worksheet, cell_range=item_range[0], font_size=item_range[2], font_name=item_range[1])

    for item_range in ACT_FOOTER_CELL_RANGES_BASIC_ALIGNMENT:
        await set_act_alignment(worksheet, item_range[0], horizontal=item_range[3], vertical=item_range[4])

    print_area = f'$A$1:M{56 + row_number}'
    break_line = 58 + row_number
    await set_act_page_after_footer_setup(worksheet, print_area, break_line)


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


async def format_act_photo_header(worksheet, row_number):
    """Форматирование строк с фото материалами

    :return:
    """
    merged_cells = [
        f'B{row_number}:E{row_number}',
        f'H{row_number}:K{row_number}',
    ]
    for merged_cell in merged_cells:
        await set_merge_cells(worksheet, merged_cell)

    photographic_materials_alignment = [
        f'B{row_number}:L{row_number}',
    ]
    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_act_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    # for item, cell_range in enumerate(photographic_materials_alignment, start=1):
    #     await set_act_range_border(worksheet, cell_range=cell_range)

    photographic_row_dimensions = [
        [f'{row_number}', "18"],
    ]
    for item in photographic_row_dimensions:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    photographic_report_font = [
        [f'B{row_number}:L{row_number}', {"font_size": "12", "bold": "True", "name": "Arial"}],
    ]
    for item, cell_range in enumerate(photographic_report_font, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])


async def format_act_photo_description(worksheet, row_number):
    """Форматирование строк с фото материалами

    :return:
    """
    merged_cells = [

        f'B{row_number}:E{row_number}',
        f'H{row_number}:K{row_number}',
    ]
    for merged_cell in merged_cells:
        await set_merge_cells(worksheet, merged_cell)

    photographic_materials_alignment = [

        f'B{row_number}:L{row_number}',
    ]
    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_act_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    # for item, cell_range in enumerate(photographic_materials_alignment, start=1):
    #     await set_act_range_border(worksheet, cell_range=cell_range)

    photographic_row_dimensions = [

        [f'{row_number}', "166"],
    ]
    for item in photographic_row_dimensions:
        await set_row_dimensions(worksheet, row_number=item[0], height=item[1])

    for item, cell_range in enumerate(photographic_materials_alignment, start=1):
        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    photographic_report_font = [
        [f'B{row_number}:L{row_number}', {"font_size": "9", "name": "Arial"}],
    ]
    for item, cell_range in enumerate(photographic_report_font, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])

    # background_color = [
    #     ["C50:H50", "FFFFC000"]
    # ]
    # for item in background_color:
    #     await set_background_color(worksheet, item[0], rgb=item[1])
