from typing import Optional

from aiogram import Dispatcher
from django.apps import AppConfig


def register(dp: Optional[Dispatcher] = None) -> None:
    """
    The function registers the app.

    :param dp:
        If Dispatcher is not None — register bots modules.
    """
    from apps.core.web.models import register_models

    register_models()

    if dp is not None:
        from .bot.filters import register_filters
        from .bot.handlers import register_handlers
        from .bot.middlewares import register_middlewares

        register_middlewares(dp)
        register_filters(dp)
        register_handlers(dp)


class Core(AppConfig):
    """Django App Config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Реестр"

    def ready(self):
        from .web import admin  # type: ignore
