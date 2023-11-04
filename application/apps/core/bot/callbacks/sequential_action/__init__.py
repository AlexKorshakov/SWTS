import asyncio
import sys
import traceback
from itertools import chain
import importlib
import os
import loader

loader.logger.debug(f"{__name__} start import")


async def run_custom_import():
    print(f'{__file__}')
    directory: str = f'{os.sep}'.join(__file__.split(f'{os.sep}')[:-1])
    moduls_path: list = list(chain(*[files for (_, _, files) in os.walk(directory)]))
    # moduls = [file.split('.')[0] for file in moduls_path if file.endswith('.py')]

    for module_name in [file.split('.')[0] for file in moduls_path if file.endswith('.py')]:
        if module_name in sys.modules: continue
        spec = importlib.util.spec_from_file_location(module_name, f'{directory}{os.sep}{module_name}.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


asyncio.run(run_custom_import())

# from . import previous_paragraph_answer
# from . import main_location_answer
# from . import main_category_answer
# from . import category_answer
# from . import general_contractors_answer
# from . import violation_category_answer
# from . import incident_level_answer
# from . import act_required_answer
# from . import elimination_time_answer
# from . import hashtags_answer
# from . import sub_location_answer
# from . import normative_documents_answer
# from . import query_post_vote
# from . import data_view_answers
#
# from . import comment
# from . import description
# from . import location
# from . import registration_finish
#
# from . import correct_registration_data_answer
# from . import correct_headlines_data_answer
# from . import correct_violations_data_answer

loader.logger.debug(f"{__name__} finish import")

# if __name__ == '__main__':
#     run_custom_import()
