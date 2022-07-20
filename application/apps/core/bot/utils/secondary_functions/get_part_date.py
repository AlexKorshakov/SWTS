from datetime import datetime


async def get_day_message():
    """Обработчик сообщений с фото
    Получение номер str дня из сообщения в формате dd
    """

    current_datetime = datetime.now()

    return str("0" + str(current_datetime.day) if current_datetime.day < 10 else str(current_datetime.day))


async def get_month_message():
    """Обработчик сообщений с фото
    Получение номер str месяца из сообщения в формате mm
    """

    current_datetime = datetime.now()
    return str("0" + str(current_datetime.month) if current_datetime.month < 10 else str(current_datetime.month))


async def get_year_message():
    """Обработчик сообщений с фото
    Получение полного пути файла
    """

    current_datetime = datetime.now()
    return str(current_datetime.year)
