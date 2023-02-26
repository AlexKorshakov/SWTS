import asyncio

from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from apps.MyBot import MyBot
from loader import logger


class ProgressBar:
    """Класс прогресс бара на основе msg.edit_text
    """

    empty_character: str = '⬜'
    complete_character: str = '🟩'

    def __init__(self, chat=None, msg=None, reply_markup=None, **kwargs: dict):
        """Инициация"""

        self.chat: int = chat
        self.msg: types.Message = msg if msg else self.start()
        self.text: str = ''
        self.reply_markup: InlineKeyboardMarkup = reply_markup
        self.kwargs: dict = kwargs

    async def start(self) -> types.Message:
        """Начало работы прогресс бара

        :return:
        """
        try:
            self.msg = await MyBot.bot.send_message(
                chat_id=self.chat,
                text=self.empty_character * 10,
                reply_markup=self.reply_markup
            )
        except RuntimeWarning as run_time_err:
            logger.error(f'{repr(run_time_err)}')

        except Exception as err:
            logger.error(f'{__class__.__name__} {repr(err)}')

        await asyncio.sleep(1)
        return self.msg

    async def finish(self) -> types.Message:
        """Окончание работы прогресс бара

        :return:
        """
        msg = await self.message_edit_text(text=self.complete_character * 10, reply_markup=self.reply_markup)
        await asyncio.sleep(1)
        return msg

    async def update_msg(self, percent: int = None) -> types.Message:
        """Обновление сообщения прогресс бара

        :param percent: int - процент выполнения
        :return:
        """

        text_green: str = self.complete_character * percent
        text_wait: str = self.empty_character * (10 - percent)

        self.msg = await self.message_edit_text(text=text_green + text_wait, reply_markup=self.reply_markup)
        await asyncio.sleep(1)
        return self.msg

    async def message_edit_text(self, text: str = '', reply_markup: InlineKeyboardMarkup = None) -> types.Message:
        """Обновление сообщения

        :param text: текст (тело) прогресс бара
        :param reply_markup:
        :return:
        """

        if not text: text = self.text
        if not reply_markup:  reply_markup = self.reply_markup

        self.msg = await self.msg.edit_text(text=text, reply_markup=reply_markup)
        await asyncio.sleep(1)
        return self.msg


async def test():
    chat = 373084462

    # msg = await MyBot.bot.send_message(chat_id=chat, text='□' * 10)
    p_bar_2 = ProgressBar(chat=chat)

    await p_bar_2.start()
    await p_bar_2.update_msg(3)
    await p_bar_2.update_msg(7)
    await p_bar_2.finish()

    # msg = await progress_bar_start(chat)
    # await progress_bar(msg, persent=1)
    # await progress_bar(msg, persent=10)


if __name__ == "__main__":

    asyncio.run(test())
