import logging
import os
import sys
from django.core.management.color import color_style

logger = logging.getLogger("django")


try:
    from config.config import BOT_TOKEN
except ModuleNotFoundError as err:
    BOT_TOKEN = None
    logger.error(f'file {os.path.basename(__file__)} err {repr(err)}')
    logger.error("Config file not found!\n"
                 "Please create config.py file according to config.py.example")

except ImportError as err:
    BOT_TOKEN = None
    logger.error(f'file {os.path.basename(__file__)} err {repr(err)}')
    logger.error(f" BOT_TOKEN {BOT_TOKEN} is not defined in the config file")

if BOT_TOKEN is None:
    raise TypeError('BOT_TOKEN Is None BOT_TOKEN не должен быть пустым!!')


class DjangoColorsFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(DjangoColorsFormatter, self).__init__(*args, **kwargs)
        self.style = self.configure_style(color_style())

    def configure_style(self, style):
        style.DEBUG = style.HTTP_NOT_MODIFIED
        style.INFO = style.HTTP_INFO
        style.WARNING = style.HTTP_NOT_FOUND
        style.ERROR = style.ERROR
        style.CRITICAL = style.HTTP_SERVER_ERROR
        return style

    def format(self, record):
        message = logging.Formatter.format(self, record)
        if sys.version_info[0] < 3:
            if isinstance(message, str):
                message = message.encode('utf-8')
        colorizer = getattr(self.style, record.levelname, self.style.HTTP_SUCCESS)
        return colorizer(message)
