import os
from multiprocessing import Process
from pathlib import Path

from apps.MyBot import MyBot
from apps.MyServer import MyServer
from apps.PeriodicCheck import PeriodicCheck
from loader import logger

BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.web.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def run_app():
    try:
        bot = Process(target=MyBot.run)
        server = Process(target=MyServer.run)
        check = Process(target=PeriodicCheck.run)

        bot.start()
        server.start()
        check.start()

    except KeyboardInterrupt as err:
        logger.errror(f'Error run_app {repr(err)}')
        exit()


if __name__ == "__main__":
    run_app()

    # bot = Process(target=MyBot.run)
    # bot.start()
