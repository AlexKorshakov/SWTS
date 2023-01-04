from openpyxl.worksheet.pagebreak import Break


async def set_act_page_setup(worksheet):
    """Установка параметров страницы

    :param worksheet:
    :return:
    """

    #  https://xlsxwriter.readthedocs.io/page_setup.html
    # worksheet.print_title_rows = '$2:$3'
    # worksheet.print_title = '$2:$3'

    # Printer Settings
    worksheet.page_setup.orientation = worksheet.ORIENTATION_PORTRAIT
    worksheet.page_setup.paperSize = worksheet.PAPERSIZE_A4

    # Подогнать область печати к определенному кол-у страниц как по вертикали, так и по горизонтали.
    worksheet.page_setup.fitToPage = True
    worksheet.page_setup.fitToHeight = '0'

    # worksheet.views
    worksheet.print_options.horizontalCentered = True
    worksheet.print_area = '$A$1:M56'

    #  масштабный коэффициент для распечатываемой страницы
    # worksheet.set_print_scale(75)

    # worksheet.row_breaks.append(Break(id=53))
    # worksheet.col_breaks.append(Break(id=13))


async def set_act_page_after_footer_setup(worksheet, print_area, break_line=None):
    """Установка параметров страницы

    :param break_line:
    :param print_area:
    :param worksheet:
    :return:
    """

    #  https://xlsxons.horizontalCentered = True
    worksheet.print_area = print_area

    #  масштабный коэффициент для распечатываемой страницы
    # worksheet.set_print_scale(75)

    if break_line:
        worksheet.row_breaks.append(Break(id=break_line))
        # worksheet.col_breaks.append(Break(id=13))