"""isort:skip_file"""
__version__ = '2.1.0'
import os
# ---------------------------------------
# Note: import order is significant here.

if not os.environ.get('PPL_PROJECT_ROOT'):
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    os.environ['PPL_PROJECT_ROOT'] = os.path.join(current_dir_path, "3rd")

# submodules
from .runtime import (
    autotune,
    Config,
    heuristics,
    JITFunction,
    KernelInterface,
    reinterpret,
    TensorWrapper,
    OutOfResources,
    MockTensor,
    pl_extension,
    Chip,
    ErrorCode,
)
from .runtime.jit import jit
from .compiler import compile, CompilationError

from . import language

__all__ = [
    "autotune",
    "cdiv",
    "CompilationError",
    "compile",
    "Config",
    "heuristics",
    "impl",
    "jit",
    "JITFunction",
    "KernelInterface",
    "language",
    "MockTensor",
    "next_power_of_2",
    "OutOfResources",
    "reinterpret",
    "runtime",
    "TensorWrapper",
    "testing",
    "tool",
    "pl_extension",
    "Chip",
    "ErrorCode",
]

# -------------------------------------
# misc. utilities that  don't fit well
# into any specific module
# -------------------------------------

def cdiv(x: int, y: int):
    return (x + y - 1) // y


def next_power_of_2(n: int):
    """Return the smallest power of 2 greater than or equal to n"""
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n |= n >> 32
    n += 1
    return n
