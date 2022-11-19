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


async def set_act_footer_values(worksheet, row_number):
    """

     :param row_number:
     :param worksheet:
     :return:
     """
    row_value = 28 + row_number

    values = [
        {'coordinate': 'B30',
         'value': 'Информацию о выполнении пунктов настоящего предписания необходимо направить '
                  'в письменной форме в адрес общества с ограниченной ответственностью «Удоканская медь» '
                  'по адресу: пгт. Новая Чара, ул. Магистральная, 21 или ',
         'row': f'{30 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'B31', 'value': 'на эл. адреса:',
         'row': f'{31 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'G31', 'value': 'тут эл.адрес выдавшего',
         'row': f'{31 - 28 + row_value}', 'column': '7'},
        {'coordinate': 'B32', 'value': 'не позднее:',
         'row': f'{32 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'G32', 'value': 'тут крайняя дата ответа',
         'row': f'{32 - 28 + row_value}', 'column': '7'},
        {'coordinate': 'B33',
         'value': 'Невыполнение предписания в установленный срок является основанием '
                  'для применения дисциплинарных взысканий',
         'row': f'{33 - 28 + row_value}', 'column': '2'},

        {'coordinate': 'B35', 'value': 'С предписанием ознакомлен: ',
         'row': f'{35 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'B36',
         'value': '(Ф.И.О, подпись должность руководителя, иного должностного лица или уполномоченного представителя '
                  'юридического лица, индивидуального предпринимателя, его уполномоченного представителя)',
         'row': f'{36 - 28 + row_value}', 'column': '2'},

        {'coordinate': 'B38', 'value': 'Сведения об отказе в ознакомлении с предписанием и отказе от подписи',
         'row': f'{38 - 28 + row_value}', 'column': '2'},

        {'coordinate': 'B40',
         'value': '(фамилия, имя, отчество (последнее – при наличии), проводившего(их) проверку или '
                  'уполномоченного выдавать предписания)',
         'row': f'{40 - 28 + row_value}', 'column': '2'},

        {'coordinate': 'B42', 'value': 'Предписание выдал: ',
         'row': f'{42 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'B43', 'value': 'тут должность выдавшего',
         'row': f'{43 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'B43', 'value': 'тут ФИО выдавшего',
         'row': f'{43 - 28 + row_value}', 'column': '11'},
        {'coordinate': 'B44', 'value': '(должность)',
         'row': f'{44 - 28 + row_value}', 'column': '2'},
        {'coordinate': 'B44', 'value': '(подпись)',
         'row': f'{44 - 28 + row_value}', 'column': '8'},
        {'coordinate': 'B44', 'value': '(расшифровка подписи)',
         'row': f'{44 - 28 + row_value}', 'column': '11'},

        {'coordinate': 'B46', 'value': 'тут дата',
         'row': f'{46 - 28 + row_value}', 'column': '11'},
        {'coordinate': 'B47', 'value': '(дата выдачи)',
         'row': f'{47 - 28 + row_value}', 'column': '11'},

        {'coordinate': 'B49', 'value': 'Экземпляр предписания для исполнения получил:',
         'row': f'{49 - 28 + row_value}', 'column': '2'},

        {'coordinate': 'B51',
         'value': '(фамилия, имя, отчество (последнее – при наличии), должность руководителя, '
                  'иного должностного лица или уполномоченного представителя юридического лица, '
                  'индивидуального предпринимателя, его уполномоченного представителя)',
         'row': f'{51 - 28 + row_value}', 'column': '2'},

        {'coordinate': 'B53', 'value': '(дата)',
         'row': f'{53 - 28 + row_value}', 'column': '11'},

        {'coordinate': 'B55', 'value': '(подпись)',
         'row': f'{55 - 28 + row_value}', 'column': '11'},
    ]

    for val in values:
        try:
            worksheet.cell(row=int(val['row']), column=int(val['column'])).value = str(val['value'])

        except Exception as err:
            logger.error(f"set_values {repr(err)}")
            return None
