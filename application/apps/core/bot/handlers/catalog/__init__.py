from loader import logger

logger.debug(f"{__name__} start import")

from . import catalog_func_handler
from . import catalog_employee
from . import catalog_employee_text
from . import catalog_normative_documents
from . import call_level_1_answer
from . import call_level_2_answer
from . import call_level_3_answer

logger.debug(f"{__name__} finish import")
