CATEGORY_ID_TRANSFORM: dict = {
    'main_category': {
        'item': 'main_category',
        'column': 'main_category_id',
        'table': 'core_maincategory',
        'description': 'Основная категория'
    },
    'location': {
        'item': 'location',
        'column': 'location_id',
        'table': 'core_location',
        'description': 'Закреплённый участок'
    },
    'main_location': {
        'item': 'main_location',
        'column': 'main_location_id',
        'table': 'core_mainlocation',
        'description': 'Площадка'
    },
    'sub_location': {
        'item': 'sub_location',
        'column': 'sub_location_id',
        'table': 'core_sublocation',
        'description': 'Под площадка / участок'
    },
    'category': {
        'item': 'category',
        'column': 'category_id',
        'table': 'core_category',
        'description': 'Категория'
    },
    'normative_documents': {
        'item': 'normative_documents',
        'column': 'normative_documents_id',
        'table': 'core_normativedocuments',
        'description': 'Под Категория'
    },
    'violation_category': {
        'item': 'violation_category',
        'column': 'violation_category_id',
        'table': 'core_violationcategory',
        'description': 'Категория нарушения'
    },
    'general_contractor': {
        'item': 'general_contractor',
        'column': 'general_contractor_id',
        'table': 'core_generalcontractor',
        'description': 'Подрядчик',
        'json_file_name': 'GENERAL_CONTRACTORS'
    },
    'act_required': {
        'item': 'act_required',
        'column': 'act_required_id',
        'table': 'core_actrequired',
        'description': 'Требуется оформление Акта-предписания?'
    },
    'incident_level': {
        'item': 'incident_level',
        'column': 'incident_level_id',
        'table': 'core_incidentlevel',
        'description': 'Уровень происшествия'
    },
    'elimination_time': {
        'item': 'elimination_time',
        'column': 'elimination_time_id',
        'table': 'core_eliminationtime',
        'description': 'Время на устранение'
    },
    'status': {
        'item': 'status',
        'column': 'status_id',
        'table': 'core_status',
        'description': 'Статус'
    },
    'work_shift': {
        'item': 'work_shift',
        'column': 'work_shift_id',
        'table': 'core_workshift',
        'description': 'Смена'
    },
    'hse_user': {
        'item': 'core_hseuser',
        'column': 'hse_user_id',
        'table': 'core_hseuser',
        'description': 'HSE'
    },
}