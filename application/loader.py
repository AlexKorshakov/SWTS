import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
