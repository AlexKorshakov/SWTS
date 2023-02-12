from loader import logger

logger.debug(f"{__name__} start import")

from . import previous_paragraph_answer
from . import main_location_answer
from . import sub_location_answer
from . import main_category_answer
from . import category_answer
from . import general_contractors_answer
from . import violation_category_answer
from . import incident_level_answer
from . import act_required_answer
from . import elimination_time_answer
from . import hashtags_answer
from . import normative_documents_answer
from . import query_post_vote
from . import data_view_answers
from . import correct_registration_data_answer
from . import correct_headlines_data_answer
from . import correct_violations_data_answer

logger.debug(f"{__name__} finish import")
