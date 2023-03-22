import asyncio
import os
import sys

import uvicorn
#  from apps.core.web.middlewares import InjectMiddleware
#  from apps.MyBot import MyBot
from config.apps import register_apps
from django.core.asgi import get_asgi_application

from loader import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.web.settings")

import nest_asyncio

nest_asyncio.apply()


#  import heartrate
#  heartrate.trace(browser=True)


class MyServer:
    """Основной класс сервера Django"""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.web.settings")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = get_asgi_application()

    config = uvicorn.Config(app=app, loop=loop, port=8001)
    server = uvicorn.Server(config=config)

    __instance = None

    def __new__(cls, val):
        if MyServer.__instance is None:
            MyServer.__instance = object.__new__(cls)
        MyServer.__instance.val = val
        return MyServer.__instance

    @classmethod
    async def run(cls):
        """Запуск основных функций сервера"""

        await cls.on_startup()
        await cls.server.serve()
        await cls.on_shutdown()

    @staticmethod
    async def on_startup() -> None:
        """Действия при запуске"""
        # InjectMiddleware.inject_params = {"bot": MyBot.bot()}

        await register_apps()

    @staticmethod
    async def on_shutdown() -> None:
        print('Server stopped')


async def test():
    try:
        my_server_task = asyncio.create_task(MyServer.run(), name='MyServer.run')
        await my_server_task

    except KeyboardInterrupt as err:
        logger.error(f'Error run_app {repr(err)}')
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(test())
