# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT


# =====================================================================================================================
from .static import (
    TYPE__VALID_VALIDATOR,
    TYPE__VALID_SOURCE_BOOL,
    TYPE__VALID_RESULT,
    TYPE__VALID_RESULT_BOOL,
    TYPE__VALID_RESULT_BOOL__EXX,
    TYPE__VALID_EXCEPTION, TYPES_ELEMENTARY_SINGLE, TYPES_ELEMENTARY_COLLECTION, TYPES_ELEMENTARY, TYPE__ELEMENTARY,
)
# ---------------------------------------------------------------------------------------------------------------------

from .value_0_explicit import (
    Explicit,
    Default,

    TYPE__EXPLICIT,
    TYPE__DEFAULT,
)

# ---------------------------------------------------------------------------------------------------------------------
# from .result_cum import (
#     # BASE
#     ResultCum,
#     # AUX
#     # TYPES
#     TYPE__RESULT_CUM_STEP,
#     TYPE__RESULT_CUM_STEPS,
#     # EXX
# )
# ---------------------------------------------------------------------------------------------------------------------
from .arrays import array_2d_get_compact_str
from .iter_aux import (
    IterAux,

    TYPE__ITERABLE_PATH_KEY,
    TYPE__ITERABLE_PATH_ORIGINAL,
    TYPE__ITERABLE_PATH_EXPECTED,
    TYPE__ITERABLE,
)


# =====================================================================================================================
