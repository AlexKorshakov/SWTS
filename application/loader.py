import json
import os
from pathlib import Path
from datetime import datetime
from datetime import timedelta, timezone
from time import localtime, strftime
from sys import stderr
from threading import current_thread

from loguru import logger as Log

from dotenv import load_dotenv

ALL = ['logger']
LOGGER_DIR = Path(__file__).resolve().parent
load_dotenv(LOGGER_DIR / "config" / ".env")

logs_path = str(os.environ.get('MAIN_DIR')) + 'logs'


def serialize(record):
    subset = {"timestamp": record["time"].timestamp(), "message": record["message"]}
    return json.dumps(subset, ensure_ascii=False)


def sink(message):
    serialized = serialize(message.record)
    print(serialized)


def aware_now():
    now = datetime.now()
    timestamp = now.timestamp()
    local = localtime(timestamp)

    try:
        seconds = local.tm_gmtoff
        zone = local.tm_zone
    except AttributeError:
        offset = datetime.fromtimestamp(timestamp) - datetime.utcfromtimestamp(timestamp)
        seconds = offset.total_seconds()
        zone = strftime("%Z")

    tz_info = timezone(timedelta(seconds=seconds), zone)
    return now.replace(tzinfo=tz_info)


Log.remove()
Log.add(
    sink=stderr, level='INFO',
    #  colorize=True,
    enqueue=True, backtrace=True
)
Log.add(
    sink=f'{logs_path}/bot_actions.log', rotation='25 MB', level='INFO', backtrace=True,
    diagnose=True,
    #  colorize=True,
    enqueue=True,
    encoding="utf8"
)
Log.add(
    f'{logs_path}/bot_errors.log', rotation='1 MB', level='ERROR', backtrace=True,
    diagnose=True,
    #  colorize=True,
    enqueue=True,
    encoding="utf8"
)
Log.add(
    f'{logs_path}/bot_debug.log', rotation='25 MB', level='DEBUG', backtrace=True,
    diagnose=True,
    #  colorize=True,
    enqueue=True,
    encoding="utf8"
)
Log.add(
    f'{logs_path}/bot_critical.log', rotation='1 MB', level='CRITICAL', backtrace=True,
    diagnose=True,
    #  colorize=True,
    enqueue=True,
    encoding="utf8"
)

# Log.add(sink)

thread = current_thread()
current_datetime = aware_now()

Log.info(f"{thread.ident = } ::: {thread.name = }")
Log.info(f'Log. {repr(Log)}')
Log.info(f"{current_datetime = } Логирование успешно настроено\n")

logger = Log

if __name__ == '__main__':
    logger.info("Логирование успешно настроено\n")
    print(1)
