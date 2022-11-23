from config.config import ADMIN_EMAIL


async def get_user_permissions(drive_service, file_id: str):
    """Получение прав на редактирование файла или папки для администратора ADMIN_EMAIL

    :param drive_service: объект авторизации
    :param file_id:
    :return: access
    """

    user_permission = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': ADMIN_EMAIL}

    access = drive_service.permissions().create(fileId=file_id,
                                                body=user_permission,
                                                fields='id',
                                                ).execute()
    return access


async def gaining_access_drive(service:object, folder_id:str):
    """Открываем доступ на редактирование файла / папки

    :param service: объект авторизации
    :param folder_id:
    :return: access
    """

    body = {'type': 'user',
            'role': 'owner',
            'emailAddress': ADMIN_EMAIL}

    access = service.permissions().create(
        fileId=folder_id,
        transferOwnership=True,
        body=body,
        fields='id'
    ).execute()

    return access
