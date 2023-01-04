

async def create_headers() -> list[dict]:
    """Подготовка заголовков таблицы отчета

    """
    data = [
        {
            "violation_id": "id записи",
            "main_category": "Основное направление",
            "category": "Категория нарушения",
            "violation_category": "Категория нарушений",
            "general_contractor": "Подрядная организация",
            "description": "Описание нарушения",
            "comment": "Комментарий",
            "incident_level": "Уровень происшествия",
            "elimination_time": "Дней на устранение",
            "act_required": "Оформление акта",
            "coordinates": "Координаты",
        }
    ]

    return data
