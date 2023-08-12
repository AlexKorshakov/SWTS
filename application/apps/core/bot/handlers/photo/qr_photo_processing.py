import os
from itertools import chain

from aiogram import types

from apps.MyBot import bot_send_message
from apps.core.bot.handlers.photo.qr_act_nom_processing import qr_act_nom_processing
from apps.core.bot.handlers.photo.qr_matrix_nom_processing import qr_matrix_nom_processing
from apps.core.bot.handlers.photo.qr_personal_id_processing import qr_personal_id_processing
from apps.core.bot.handlers.photo.qr_worker import qr_code_reader, read_qr_code_image
from apps.core.bot.messages.messages import Messages
from apps.core.bot.messages.messages_test import msg
from apps.core.settyngs import get_sett
from apps.core.utils.secondary_functions.get_filepath import create_file_path, BOT_MEDIA_PATH


async def qr_code_processing(message: types.Message, context: dict = None) -> bool:
    """Функция распознавания qr-кодов

    """

    hse_user_id = message.chat.id

    if not get_sett(cat='enable_features', param='use_qr_code_processing').get_set():
        msg_text: str = await msg(hse_user_id, cat='error', msge='features_disabled',
                                  default=Messages.Error.features_disabled).g_mas()
        await bot_send_message(chat_id=hse_user_id, text=msg_text, disable_web_page_preview=True)
        return False

    photo_file_path = f"{BOT_MEDIA_PATH}qr_code\\{hse_user_id}\\photos\\"

    await create_file_path(path=photo_file_path)
    await message.photo[-1].download(make_dirs=False, destination_file=f"{photo_file_path}\\{hse_user_id}.jpg")

    img = read_qr_code_image(f"{photo_file_path}\\{hse_user_id}.jpg")
    data: list = await qr_code_reader(hse_user_id, img)

    if not data:
        answer_text: str = await msg(
            hse_user_id, cat='warning', msge='qr_not_found', default="QR-код, не распознан или отсутствует").g_mas()

        await bot_send_message(chat_id=hse_user_id, text=answer_text)
        try:
            os.remove(photo_file_path)
        except PermissionError:
            pass
        return False

    if not isinstance(data, list):
        return False

    qr_dat = [item for item in list(chain(*data)) if 'qr_matrix_nom_' in item]
    if qr_dat:
        await qr_matrix_nom_processing(hse_user_id, qr_data=data)

    qr_dat = [item for item in list(chain(*data)) if 'qr_act_nom_' in item]
    if qr_dat:
        await qr_act_nom_processing(hse_user_id, data=data)

    qr_dat = [item for item in list(chain(*data)) if 'personal_id_code_' in item]
    if qr_dat:
        await qr_personal_id_processing(hse_user_id, data=data, message=message)
        return True

    qr_dat = [item for item in data if 'personal_id_code_' in item]
    if qr_dat:
        await qr_personal_id_processing(hse_user_id, data=data, message=message)
        return True

    try:
        os.remove(f'{photo_file_path}\\{hse_user_id}.jpg')
    except PermissionError:
        pass

    return True
