from loader import logger


async def set_act_body_values(worksheet):
    """

    :param worksheet:
    :return:
    """
    values = [
        {'coordinate': 'B6', 'value': 'Акт предписание № от', 'row': '6', 'column': '2'},
        {'coordinate': 'B7', 'value': 'об устранении нарушений ', 'row': '7', 'column': '2'},

        {'coordinate': 'B9', 'value': 'тут наименование организации', 'row': '9', 'column': '2'},
        {'coordinate': 'B10',
         'value': '(указать кому адресовано (полное или сокращенное наименование юридического '
                  'лица либо индивидуального предпринимателя, ИНН) ',
         'row': '10', 'column': '2'},
        {'coordinate': 'B11', 'value': 'Мною:', 'row': '11', 'column': '2'},
        {'coordinate': 'B12', 'value': 'тут должность и ФИО полностью выдавшего', 'row': '12', 'column': '2'},

        {'coordinate': 'B14',
         'value': '(фамилия, имя, отчество (последнее – при наличии), должность должностного '
                  'лица, уполномоченного выдавать предписания',
         'row': '14', 'column': '2'},
        {'coordinate': 'B15', 'value': 'проведена проверка по соблюдению требований ОТ, ПБ и ООС, в отношении:',
         'row': '15', 'column': '2'},
        {'coordinate': 'B16', 'value': 'тут наименование организации', 'row': '16', 'column': '2'},
        {'coordinate': 'B17',
         'value': '(указать полное наименование юридического лица либо индивидуального предпринимателя)', 'row': '17',
         'column': '2'},

        {'coordinate': 'B19', 'value': 'В присутствии:', 'row': '19', 'column': '2'},
        {'coordinate': 'B20', 'value': 'тут ответственный', 'row': '20', 'column': '2'},

        {'coordinate': 'B22', 'value': 'ПРЕДПИСЫВАЕТСЯ ', 'row': '22', 'column': '2'},
        {'coordinate': 'B23', 'value': 'Принять меры по устранению выявленных нарушений в установленные сроки.',
         'row': '23', 'column': '2'},

        {'coordinate': 'B25', 'value': '№', 'row': '25', 'column': '2'},
        {'coordinate': 'B25', 'value': 'Описание и характер выявленных нарушений', 'row': '25', 'column': '3'},
        {'coordinate': 'B25',
         'value': 'Наименование НПА, номера подпунктов, пунктов, требования которых нарушены или не соблюдены',
         'row': '25', 'column': '6'},
        {'coordinate': 'B25', 'value': 'Предписываемые меры по устранению выявленного нарушения', 'row': '25',
         'column': '9'}, {'coordinate': 'B25', 'value': 'Срок устранения нарушений', 'row': '25', 'column': '12'},
        {'coordinate': 'B26', 'value': 'п/п', 'row': '26', 'column': '2'},
        {'coordinate': 'B27', 'value': 'тут наименование ПО', 'row': '27', 'column': '2'},
        {'coordinate': 'B28', 'value': '1', 'row': '28', 'column': '2'},
    ]

    for val in values:
        try:
            worksheet.cell(row=int(val['row']), column=int(val['column'])).value = str(val['value'])

        except Exception as err:
            logger.error(f"set_values {repr(err)}")
            return None


