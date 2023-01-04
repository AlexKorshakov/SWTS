from aiogram import Bot, Dispatcher
from aiogram.utils import executor

from apps.core.bot.messages.messages import Messages
from apps.core.bot.middlewares import setup_middlewares
from apps.core.utils import on_startup_notify
from apps.core.utils.bot_utils_processor.set_bot_commands import set_default_commands
from apps.xxx import assistant, dp_assistant
from config.config import SKIP_UPDATES
from loader import logger


class MyBot:
    # storage = MemoryStorage()
    # bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    # dp = Dispatcher(bot=bot, storage=storage)
    bot = assistant
    dp = dp_assistant

    Bot.set_current(bot)
    Dispatcher.set_current(dp)

    @classmethod
    def run(cls):
        try:
            executor.start_polling(
                dispatcher=cls.dp,
                on_startup=cls.on_startup,
                on_shutdown=cls.on_shutdown,
                skip_updates=SKIP_UPDATES,
                allowed_updates=cls.get_handled_updates_list(cls.dp)
            )
        except Exception as err:
            logger.error(f"Bot start Exception {repr(err)}")

        # finally:
        #     with suppress(RuntimeWarning, DeprecationWarning):
        #         cls.dp.storage.close()
        #         cls.dp.storage.wait_closed()
        #         cls.bot.session.close()

    @staticmethod
    async def on_startup(dp: Dispatcher):
        logger.info("Установка обработчиков...")
        print("Установка обработчиков...")
        try:
            import apps.core.bot.filters
            import apps.core.bot.callbacks
            import apps.core.bot.handlers
            logger.info("Все части зарегистрированы...")
        except Exception as err:
            logger.warning(f'Exception in app.py {err}')
            quit()

        setup_middlewares(dp)
        await on_startup_notify(dp)
        await set_default_commands(dp)

        logger.info(Messages.Successfully.bot_start)
        print(Messages.Successfully.bot_start)

        # await register_apps(dp)

    @staticmethod
    def get_handled_updates_list(dp: Dispatcher):
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
        await dp.storage.close()
        await dp.storage.wait_closed()
        quit()
