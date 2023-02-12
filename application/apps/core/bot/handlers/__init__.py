from loader import logger

logger.debug(f"{__name__} start import")
from . import errors
from . import cancel
from . import admin_func
from . import photo
from . import start
from . import help
from . import send_mail
from . import generate_act
from . import generate_report
from . import generate_statistic
from . import correct_entries
from . import developer
from . import text

logger.debug(f"{__name__} finish import")
