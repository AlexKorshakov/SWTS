import asyncio

from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from apps.MyBot import bot_send_message
from apps.core.bot.bot_utils.progress_bar import ProgressBar
from apps.core.bot.reports.report_data_preparation import get_vio_atr_data


import reportlab

from reportlab.pdfgen.canvas import Canvas

canvas = Canvas("hello.pdf")


def main():
    # menu_list = get_data_list("VIOLATION_CATEGORY")
    # pprint(menu_list)
    data = get_vio_atr_data("main_location")
    print(data)


async def message_edit_text(message: types.Message, text: str, reply_markup: InlineKeyboardMarkup = None) -> bool:
    """

    :param message:
    :param text:
    :param reply_markup:
    :return:
    """

    if message is None:
        return False

    if not text:
        return False

    try:
        await message.edit_text(text=text, reply_markup=reply_markup)
        return True
    except Exception as err:
        print(f'{repr(err)}')


async def progress_bar_for_range(message: types.Message):
    reply_markup = None

    for i in range(1, 11):
        text_green = '🟩' * i
        text_wait = '⬜' * (10 - i)

        text = text_green + text_wait
        await message.edit_text(text=text, reply_markup=reply_markup)
        await asyncio.sleep(1)


async def progress_bar_start(chat, persent=0):
    if not chat:
        return None

    text = '⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜'
    msg = await bot_send_message(chat_id=chat, text=text)
    await asyncio.sleep(1)
    return msg


async def progress_bar(message: types.Message, persent=4):
    reply_markup = None

    if not persent:
        return False

    text_green = '🟩' * persent
    text_wait = '⬜' * (10 - persent)

    text = text_green + text_wait
    await message.edit_text(text=text, reply_markup=reply_markup)
    await asyncio.sleep(1)
    return True


async def test():
    chat = 373084462

    msg = await bot_send_message(chat_id=chat, text='□' * 10)
    p_bar = ProgressBar(msg=msg)

    # await p_bar.start()
    await p_bar.update_msg(3)
    await p_bar.update_msg(7)
    await p_bar.finish()

    p_bar_2 = ProgressBar(chat=chat)

    await p_bar_2.start()
    await p_bar_2.update_msg(3)
    await p_bar_2.update_msg(7)
    await p_bar_2.finish()

    # msg = await progress_bar_start(chat)
    # await progress_bar(msg, persent=1)
    # await progress_bar(msg, persent=10)


if __name__ == "__main__":
    # main()

    asyncio.run(test())

    # isort.file("test_2.py")
