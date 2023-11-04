import asyncio
import importlib
import os
import sys
import traceback
from itertools import chain

import loader

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

    # await MyBot.bot.set_my_commands([types.BotCommand(command="/catalog", description="Справочник")])


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


asyncio.run(run_custom_import())



# from loader import logger
#
# logger.debug(f"{__name__} start import")
#
# from . import correct_entries_handler
# from . import correct_item_violations
# from . import correct_violations
# #
# # from . import correct_non_act_item
# # from . import correct_non_act_item_finalize
# # from . import correct_non_act_item_item_correct
# # from . import correct_non_act_item_delete
# #
# # from . import correct_acts
# # from . import correct_act_delete
# # from . import correct_act_delete_from_base
# # from . import correct_act_finalize
# # from . import correct_act_download
# #
# from . import correct_act_item_correct
# # from . import correct_act_item_delete
# # from . import correct_act_item_data_correct
# # from . import correct_act_item_finalize
# #
# # from . import correct_violations_complex_meaning_handler
# # from . import correct_violations_text_meaning_handler
# # # from . import correct_violations_special_meaning_handler
# # from . import correct_violations_simple_meaning_handler
# #
# #
# logger.debug(f"{__name__} finish import")
# #