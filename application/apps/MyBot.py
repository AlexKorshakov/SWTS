from __future__ import annotations

import asyncio
import sys
import traceback
from pprint import pprint

import aiohttp
import nest_asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatActions, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from apps.core.bot.messages.messages import Messages
from apps.core.bot.messages.messages_test import msg
from apps.core.bot.middlewares import setup_middlewares
from apps.core.set_bot_commands import set_default_commands
from apps.core.settyngs import get_sett
from apps.notify_admins import on_startup_notify_admins
from apps.xxx import assistant, dp_assistant
from config.config import SKIP_UPDATES
from loader import logger

nest_asyncio.apply()


# import heartrate
# heartrate.trace(browser=True)


class MyBot:
    """Основной класс запуска бота

    """
    bot = assistant
    dp = dp_assistant

    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    name = 'STNGBot'
    __instance = None

    def __new__(cls, val):
        if MyBot.__instance is None:
            MyBot.__instance = object.__new__(cls)
        MyBot.__instance.val = val
        return MyBot.__instance

    @classmethod
    def get_name(cls):
        return cls.dp.bot._me.first_name

    @classmethod
    async def run(cls):
        """Сборка и запуск бота"""
        try:
            await executor.start_polling(
                dispatcher=cls.dp,
                on_startup=cls.on_startup,
                on_shutdown=cls.on_shutdown,
                timeout=200,
                skip_updates=SKIP_UPDATES,
                allowed_updates=await cls.get_handled_updates_list(cls.dp)
            )
        except RuntimeWarning as err:
            logger.error(f"Bot start RuntimeWarning {repr(err)}")

        except aiohttp.client_exceptions.ClientConnectorError as err:
            logger.error(f"Bot start ClientConnectorError {repr(err)}")

        except Exception as err:
            logger.error(f"Bot start Exception {repr(err)}")

        finally:
            # with suppress(RuntimeWarning, DeprecationWarning):
            await cls.dp.storage.close()
            await cls.dp.storage.wait_closed()
            await cls.bot.session.close()

    @staticmethod
    async def on_startup(dp: Dispatcher):
        logger.info(f"{dp.bot._me.first_name} started Установка обработчиков...")
        print(f"{dp.bot._me.first_name} Установка обработчиков...")
        try:
            import apps.core.bot.filters
            import apps.core.bot.callbacks
            import apps.core.bot.handlers
            logger.info(f"{dp.bot._me.first_name} Все части зарегистрированы...")

        except Exception as err:
            logger.warning(f'{dp.bot._me.first_name} Exception in app.py {err}')
            sys.exit()

        await setup_middlewares(dp)
        await on_startup_notify_admins(dp)
        await set_default_commands(dp)

        on_startup_text: str = f'{dp.bot._me.first_name} {Messages.Successfully.bot_start}'
        logger.info(on_startup_text)
        print(on_startup_text)

        # await register_apps(dp)

    @staticmethod
    async def get_handled_updates_list(dp: Dispatcher):
        """
        Here we collect only the needed updates for bot based on already registered handlers types.
        This way Telegram doesn't send unwanted updates and bot doesn't have to proceed them.

        Здесь мы собираем только необходимые обновления для бота на основе уже зарегистрированных типов обработчиков.
        Таким образом, Telegram не отправляет нежелательные обновления, и боту не нужно их обрабатывать.
        :param dp: Dispatcher
        :return: a list of registered handlers types
        """
        available_updates = (
            "callback_query_handlers",
            "channel_post_handlers",
            "chat_member_handlers",
            "chosen_inline_result_handlers",
            "edited_channel_post_handlers",
            "edited_message_handlers",
            "inline_query_handlers",
            "message_handlers",
            "my_chat_member_handlers",
            "poll_answer_handlers",
            "poll_handlers",
            "pre_checkout_query_handlers",
            "shipping_query_handlers",
        )
        return [item.replace("_handlers", "") for item in available_updates
                if len(dp.__getattribute__(item).handlers) > 0]

    @staticmethod
    async def on_shutdown(dp: Dispatcher):
        logger.warning('Bye! Shutting down connection')
        logger.warning(f'{dp.bot._me.first_name} Bye! Shutting down connection')
        await dp.storage.close()
        await dp.storage.wait_closed()
        sys.exit()


async def bot_send_document(*, chat_id: int | str, doc_path: str, caption: str = None, fanc_name: str = None,
                            **kvargs) -> bool:
    """Функция отправки документов

    :param fanc_name:
    :param caption:
    :param chat_id:
    :param doc_path:
    :return:
    """

    await MyBot.bot.send_chat_action(chat_id=chat_id, action=ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(2)  # скачиваем файл и отправляем его пользователю

    try:
        with open(file=doc_path, mode='rb') as doc:
            result: types.Message | None = await MyBot.bot.send_document(
                chat_id=chat_id, document=doc, caption=caption, **kvargs
            )

        logger.info(f"{MyBot.get_name()} {chat_id = } {calling_fanc_name} {caption} отправлен отчет {doc}")

    except OSError as err:
        logger.error(f"{MyBot.get_name()} {calling_fanc_name} {repr(err)}")
        return False

    except Exception as err:
        logger.error(f"{MyBot.get_name()} {calling_fanc_name} {repr(err)}")
        return False

    if result:
        return True
    return False


async def bot_send_photo(*, chat_id: int | str, photo=None, caption: str = None) -> bool:
    """Используйте этот метод для отправки текстовых сообщений.
    Источник: https://core.telegram.org/bots/api#sendmessage

    """

    await MyBot.bot.send_chat_action(chat_id=chat_id, action=ChatActions.UPLOAD_PHOTO)
    await asyncio.sleep(2)  # скачиваем файл и отправляем его пользователю

    try:
        result: types.Message | None = await MyBot.bot.send_photo(
            chat_id=chat_id, photo=photo, caption=caption
        )

    except OSError as err:
        logger.error(f"{MyBot.get_name()}  {repr(err)}")
        return False

    except Exception as err:
        logger.warning(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return False

    if result:
        return True
    return False


async def bot_send_message(*, chat_id: int | str, text: str,
                           reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
                           **kvargs) -> bool:
    """Используйте этот метод для отправки текстовых сообщений.
    Источник: https://core.telegram.org/bots/api#sendmessage

    """

    try:
        result: types.Message | None = await _send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup, **kvargs
        )

    except Exception as err:
        logger.warning(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return False

    if result:
        return True
    return False


async def _send_message(*, chat_id: int | str, text: str,
                        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
                        **kvargs) -> types.Message | None:
    """Отправка сообщения

    :param chat_id:
    :param text:
    :param reply_markup:
    :param kvargs:
    :return:
    """
    try:
        result: types.Message | None = await MyBot.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup, **kvargs
        )
        return result

    except Exception as err:
        logger.error(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return None


async def bot_delete_message(*, chat_id: int | str, message_id: int | str, sleep_sec: int = 5) -> bool:
    """Используйте этот метод для удаления сообщения, в том числе служебного, со следующими ограничениями:
         - Сообщение может быть удалено только в том случае, если оно было отправлено менее 48 часов назад.
         - Боты могут удалять исходящие сообщения в приватных чатах, группах и супергруппах.
         - Боты могут удалять входящие сообщения в приватных чатах.
         - Боты с разрешениями can_post_messages могут удалять исходящие сообщения в каналах.
         - Если бот является администратором группы, он может удалить там любое сообщение.
         - Если у бота есть разрешение can_delete_messages в супергруппе или канале, он может удалить там любое сообщение.
    Источник: https://core.telegram.org/bots/api#deletemessage

        :param sleep_sec:
        :param chat_id: Unique identifier for the target chat or username of the target channel
        :type chat_id: :obj:`typing.Union[base.Integer, base.String]`
        :param message_id: Identifier of the message to delete
        :type message_id: :obj:`base.Integer`
        :return: Returns True on success
        :rtype: :obj:`base.Boolean`
    :return:
    """

    if not get_sett(cat='enable_features', param='bot_delete_message').get_set():
        msg_text: str = await msg(chat_id, cat='error', msge='features_disabled',
                                  default=Messages.Error.features_disabled).g_mas()
        logger.warning(f'{MyBot.get_name()} {chat_id = } {msg_text = }')
        return False

    if sleep_sec:
        await asyncio.sleep(sleep_sec)

    try:
        result: types.Message | None = await MyBot.bot.delete_message(chat_id=chat_id, message_id=message_id)

    except Exception as err:
        logger.warning(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return False

    if result:
        return True
    return False


async def bot_delete_markup(message: types.Message, sleep_sec: int = None):
    """Удаление клавиатуры сообщения

    :param sleep_sec:
    :param message:
    :return:
    """
    # удаляем кнопки у последнего сообщения
    chat_id = message.chat.id

    if sleep_sec:
        await asyncio.sleep(sleep_sec)

    try:
        result = await MyBot.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message.message_id - 1,
            reply_markup=None
        )
    except MessageNotModified as err:
        logger.warning(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return False

    except MessageToEditNotFound as err:
        logger.warning(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return False

    except Exception as err:
        logger.warning(f'{MyBot.get_name()} {chat_id = } {repr(err)}')
        return False

    if result:
        return True
    return False


async def fanc_name() -> str:
    """Возвращает имя вызываемой функции"""
    stack = traceback.extract_stack()
    return str(stack[-2][2])


async def test():
    try:
        my_bot_task = asyncio.create_task(MyBot.run(), name='MyBot.run')
        await my_bot_task

    except KeyboardInterrupt as err:
        logger.error(f'Error run_app {repr(err)}')
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(test())
