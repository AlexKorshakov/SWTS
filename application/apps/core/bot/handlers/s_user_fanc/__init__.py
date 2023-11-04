# from loader import logger
#
# logger.debug(f"{__name__} start import")
#
# from . import s_user_fanc
# from . import s_user_enable_features
# from . import s_user_get_files
# from . import s_user_get_current_file
# from . import s_user_set_current_file
# from . import s_user_bot_comands
#
# logger.debug(f"{__name__} finish import")
import asyncio
import sys
import traceback
from itertools import chain
import importlib
import os

from aiogram import types

import loader
from apps.MyBot import MyBot

loader.logger.debug(f"{__name__} start import")


async def run_custom_import():
    print(f'{await fanc_name()} :: {__file__}')

    directory: str = f'{os.sep}'.join(__file__.split(f'{os.sep}')[:-1])
    moduls_path: list = list(chain(*[files for (_, _, files) in os.walk(directory)]))

    for module_name in [file.split('.')[0] for file in moduls_path if file.endswith('.py')]:
        if module_name in sys.modules: continue
        spec = importlib.util.spec_from_file_location(module_name, f'{directory}{os.sep}{module_name}.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    # await MyBot.bot.set_my_commands([types.BotCommand(command="/super_user_fanc", description="Админка2")])


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


asyncio.run(run_custom_import())
