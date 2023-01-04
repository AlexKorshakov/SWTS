class Messages:
    """Класс со всеми текстовыми сообщениями
    """
    url_registration_violation: str = f"https://www.youtube.com/channel/UCbq0Z7aDzYc3S4dAPTFDtkA"

    write_to_developer: str = f'Чтобы написать разработчику нажмите /developer'
    help_message: str = f"Справка по командам бота /help \n" \
                        f'\n' \
                        f"Видео инструкция {url_registration_violation}" \
                        f'\n' \
                        f'{write_to_developer}'
                        # f'Для регистрации в системе (повторной регистрации) нажмите /start \n' \
    wait: str = f"Это может занять некоторое время"
    cancel: str = f"Отмена!"
    correct_cancel: str = f"продолжить без изменений"
    hi: str = f"Привет"
    user_greeting: str = f'Этот бот предназначен для регистрации нарушений и создания ежедневных отчетов \n' \
                         f'Для начала работы просто отправьте фото боту'

    bot_setting_commands: str = 'Установка команд бота...'

    defined_recipient_list: str = 'Определён список получателей'
    all_canceled: str = f"Все действия отменены"

    class Registration:
        user_registration: str = f"Начинаю процедуру регистрации"
        confirm: str = f"При завершении регистрации дальнейшее изменение невозможно!"
        canceled: str = f"OK! если хотите зарегистрироваться, отправьте /start заново"
        cancel: str = f"Отменить регистрацию"

    class Violations:
        canceled: str = f"Изменения отменены"

    class Viewer:
        canceled: str = f"Действия отменены"

    class Removed:
        violation_data_pc: str = "Запись о нарушении удалена с сервера"
        violation_photo_pc: str = "Фотоматериалы нарушения удалены с сервера"
        violation_data_gdrive_delete: str = "Запись о нарушении удалена с Google Drive"
        violation_photo_gdrive: str = "Фотоматериалы нарушения удалены с Google Drive"

    class Ask:
        name: str = f"Введите ваше ФИО полностью"
        function: str = f"Введите вашу должность полностью"
        phone_number: str = f"Введите свой номер телефона с кодом (в формате +7xxxxxxxxxx)"
        work_shift: str = f"Выберите в  какую смену вы работаете? (пример дневная смена / ночная смена)"
        location: str = f"Выберите ваше местоположение"
        construction_manager: str = f"Введите ФИО руководителя строительства полностью"
        building_control_engineer: str = f"Введите полностью ФИО инженера строительного контроля"
        contractor: str = f'Выберите подрядчика из списка'
        subcontractor: str = f"Введите полностью наименование субподрядчика "
        linear_bypass: str = f"Введите наименование линейного обхода. Например Первичный"
        date_linear_bypass: str = f"Введите дату проведения линейного обхода. Например 12.12.2021"
        contractor_representative = f"Введите ФИО и должность представителя подрядчика полностью." \
                                    f" Например Иванов Иван Иванович. Технический директор"
        subcontractor_representative: str = f"Введите ФИО и должность представителя субподрядчика полностью." \
                                            f" Например Иванов Иван Иванович. Технический директор"

    class Report:
        create_successfully: str = f"Отчет сформирован на сервере"
        done: str = 'Процедура завершена'
        start: str = f"Начинаю генерацию отчетов"
        start_act: str = 'Начало генерации актов-предписания'
        sent_successfully: str = f"Отчет успешно отправлен"
        generated_successfully: str = f"Отчет успешно создан"
        begin: str = f"Запись загружается"
        completed_successfully: str = f"Запись загружена"
        convert_successfully: str = f"Отчет успешно конвертирован в pdf"
        error: str = 'не удалось конвертировать отчет в pdf'
        acts_generated_successfully: str = 'Акт(-ы) успешно созданы'

    class HSEUserAnswer:
        user_access_success: str = f"Вам предоставлен доступ к функциям"

    class Successfully:
        bot_start: str = f"Бот успешно запущен..."
        save_data_on_g_drive: str = "Данные сохранены в Google Drive"
        registration_completed: str = "Регистрация прошла успешно"
        correct_registration_completed: str = "Изменение данных регистрации прошло успешно"
        correct_headlines_completed: str = "Изменение данных шапки отчета прошло успешно"
        correct_violations_completed: str = "Изменение данных нарушения прошло успешно"
        registration_data_received: str = "Регистрационные данные получены"
        list_tutors_received: str = "Список получателей получен"
        mail_send: str = "Письмо с отчетами успешно отправлено"
        letter_formed: str = "Письмо сформировано"

    class Enter:
        comment: str = "Введите комментарий к устранению"
        description_violation: str = "Введите описание нарушения"

    class Admin:
        answer: str = f"Выберите действие"

    class Choose:
        main_location: str = f"Выберите основную локацию"
        main_category: str = f"Выберите основную категорию"
        entry: str = f"Выберите запись или действие для корректировки"
        elimination_time: str = f"Выберите количество дней на устранение"
        violation_category: str = f"Выберете степень опасности ситуации"
        normative_documents: str = f"Выберете нарушение нажав на кнопку соответствующего нарушения"
        sub_location: str = f"Выберете площадку нажав на соответствую кнопку "
        act_required: str = f"Выберите требуется ли оформление акта - предписания"
        general_constractor: str = f"Выберите подрядную организацию"
        category: str = f"Выберите категорию нарушения"
        incident_level: str = f"Выберите уровень происшествия"

    class Error:
        workbook_not_found: str = f"Файл с отчетом не найден! Обратитесь к разработчику! \n" \
                                  f'чтобы написать разработчику нажмите /developer'
        worksheet_not_found: str = f"Страница с отчетом не найден! Обратитесь к разработчику! \n" \
                                   f'чтобы написать разработчику нажмите /developer'
        fill_report_path_not_found: str = f"Путь к файлу с отчетом не найден! Обратитесь к разработчику! \n" \
                                          f'чтобы написать разработчику нажмите /developer'
        dataframe_not_found: str = f'Не удалось получить массив данных для формирования отчета! \n' \
                                   'Обратитесь к разработчику! \n' \
                                   f'чтобы написать разработчику нажмите /developer'
        file_list_not_found: str = f"Список файлов не найден! \n"
        workbook_not_create: str = f"Файл с отчетом не создан! Обратитесь к разработчику! \n" \
                                   f'чтобы написать разработчику нажмите /developer'

        registration_file_list_not_found: str = "Не удалось получить регистрационные данные!" \
                                                " Обратитесь к разработчику! \n" \
                                                f'чтобы написать разработчику нажмите /developer'
        authorized_google_drive: str = f"Не удалось авторизоваться на Google Drive!"
        upload_on_web: str = "Файл не обнаружен, загрузка на web прервана"
        file_not_found: str = "Файлы не найдены. Вероятно они были удалены"
        data_not_found: str = "Данные для составления Акта не найдены."
        location_name_not_found: str = "Не найдены данные о местоположении!"
        invalid_input: str = f"Отправь мне свой номер телефона с кодом (пример +7xxxxxxxxxx)"
        no_file_too_send: str = "Нет файлов для отправки"

        list_too_send_not_found: str = f"Не найден список получателей!\n Пройдите процедуру регистрации повторно" \
                                       f"Для регистрации нажмите /start" \
                                       f"Если ошибка повторится обратитесь к разработчику " \
                                       f"Чтобы написать разработчику нажмите /developer"
