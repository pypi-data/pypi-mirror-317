# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT


# =====================================================================================================================
from .info import (
    ObjectInfo,

    ItemInternal,
    ObjectState,
)
from .obj_types import (
    TYPES,
    TypeCheck,
)

# ---------------------------------------------------------------------------------------------------------------------
from .primitives import (
    # RANGES ---
    RANGE0,
    RANGE1,
    RANGE2,
    RANGE3,

    # SETS -----
    VALUES_BLANK,
    VALUES_BLANK__ELEMENTARY_SINGLE,
    VALUES_BLANK__ELEMENTARY_COLLECTION,

    VALUES_NOT_BLANK,
    VALUES_NOT_BLANK__ELEMENTARY_SINGLE,
    VALUES_NOT_BLANK__ELEMENTARY_COLLECTION,
    VALUES__ELEMENTARY_SINGLE,

    VALUES_CALLABLE,

    # FUNCS ----
    GEN_COMPR,

    FUNC,
    FUNC_NONE, FUNC_TRUE, FUNC_FALSE, FUNC_ECHO,
    FUNC_EXX, FUNC_RAISE,
    FUNC_ALL,
    FUNC_ANY,
    FUNC_LIST_DIRECT,
    FUNC_LIST_VALUES,
    FUNC_DICT,
    FUNC_GEN,

    # LAMBDAS ----
    LAMBDA_ARGS,
    LAMBDA_KWARGS,

    LAMBDA,
    LAMBDA_NONE, LAMBDA_TRUE, LAMBDA_FALSE, LAMBDA_ECHO,
    LAMBDA_EXX, LAMBDA_RAISE,
    LAMBDA_ALL,
    LAMBDA_ANY,
    LAMBDA_LIST_DIRECT,
    LAMBDA_LIST_VALUES,
    LAMBDA_DICT,
    LAMBDA_GEN,

    # CLS -----
    ClsInt,
    ClsFloat,
    ClsStr,
    ClsList,
    ClsTuple,
    ClsSet,
    ClsDict,

    CLASSES__AS_FUNC,

    ClsInitArgsKwargs,
    ClsInitRaise,

    # CLS with INST -----
    ClsException, INST_EXCEPTION,

    Cls, INST,
    ClsEmpty, INST_EMPTY,

    ClsCall, INST_CALL,
    ClsCallNone, INST_CALL_NONE,
    ClsCallTrue, INST_CALL_TRUE,
    ClsCallFalse, INST_CALL_FALSE,
    ClsCallExx, INST_CALL_EXX,
    ClsCallRaise, INST_CALL_RAISE,

    ClsBoolTrue, INST_BOOL_TRUE,
    ClsBoolFalse, INST_BOOL_FALSE,
    ClsBoolRaise, INST_BOOL_RAISE,

    ClsIterYield, INST_ITER_YIELD,
    ClsIterArgs, INST_ITER_ARGS,
    ClsGen, INST_GEN,

    ClsEq, INST_EQ,
    ClsEqTrue, INST_EQ_TRUE,
    ClsEqFalse, INST_EQ_FALSE,
    ClsEqRaise, INST_EQ_RAISE,

    ClsFullTypes, INST_FULL_TYPES,
)


# =====================================================================================================================
