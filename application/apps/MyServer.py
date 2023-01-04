import asyncio

import uvicorn
from django.core.asgi import get_asgi_application

from apps.MyBot import MyBot
from apps.core.web.middlewares import InjectMiddleware
from config.apps import register_apps

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class MyServer:
    app = get_asgi_application()

    config = uvicorn.Config(app=app, loop=loop, port=8001)
    server = uvicorn.Server(config=config)

    @classmethod
    def run(cls):
        asyncio.run(cls.on_startup())
        asyncio.run(cls.server.serve())
        # asyncio.run(cls.on_shutdown())

    @staticmethod
    async def on_startup() -> None:
        InjectMiddleware.inject_params = dict(bot=MyBot.bot)

        await register_apps()

    # @staticmethod
    # async def on_shutdown() -> None:
    #     pass
