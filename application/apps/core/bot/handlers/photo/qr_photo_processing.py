import os

from aiogram import types

from apps.MyBot import bot_send_message
from apps.core.bot.handlers.photo.qr_worker import qr_code_reader, read_qr_code_image, generate_text
from apps.core.utils.secondary_functions.get_filepath import create_file_path, BOT_MEDIA_PATH


async def qr_code_processing(message: types.Message, context: dict = None) -> bool:
    """

    """

    hse_user_id = message.chat.id

    photo_file_path = f"{BOT_MEDIA_PATH}qr_code\\{hse_user_id}\\photos\\"

    await create_file_path(path=photo_file_path)
    await message.photo[-1].download(make_dirs=False, destination_file=f"{photo_file_path}\\{hse_user_id}.jpg")

    img = read_qr_code_image(f"{photo_file_path}\\{hse_user_id}.jpg")
    data: list = qr_code_reader(img)

    if not data:
        answer_text = "QR-код, не распознан или отсутствует"
        await bot_send_message(chat_id=hse_user_id, text=answer_text)
        try:
            os.remove(photo_file_path)
        except PermissionError:
            pass
        return False

    answer_text: str = await generate_text(qr_data=data)

    for item_txt in await text_processor(text=answer_text):
        await bot_send_message(chat_id=hse_user_id, text=item_txt)

    if not answer_text:
        answer_text = "QR-код, не распознан или отсутствует"
        await bot_send_message(chat_id=hse_user_id, text=answer_text)
        try:
            os.remove(photo_file_path)
        except PermissionError:
            pass
        return False

    try:
        os.remove(f'{photo_file_path}\\{hse_user_id}.jpg')
    except PermissionError:
        pass

    # await bot_send_message(chat_id=hse_user_id, text=answer_text)

    return True

    # find_data_in_dataframe(update, answer_text=data)


async def text_processor(data_list_to_text: list = None, text: str = None) -> list:
    """Принимает data_list_to_text[] для формирования текста ответа
    Если len(text) <= 3500 - отправляет [сообщение]
    Если len(text) > 3500 - формирует list_with_parts_text = []

    :param text:
    :param data_list_to_text: лист с данными для формирования текста сообщения
    :return: list - list_with_parts_text
    """

    if not text:
        text = '\n\n'.join(str(item[0]) + " : " + str(item[1]) for item in data_list_to_text)

    if len(text) <= 3500:
        return [text]

    text = ''
    list_with_parts_text = []
    for item in data_list_to_text:

        text = text + f' \n\n {str(item[0])} : {str(item[1])}'
        if len(text) > 3500:
            list_with_parts_text.append(text)
            text = ''

    return list_with_parts_text