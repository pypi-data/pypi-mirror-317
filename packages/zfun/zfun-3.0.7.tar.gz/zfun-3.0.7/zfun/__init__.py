import inspect

import zfun.funs as funs
from zfun.funs import *

__all__ = [n for n, _ in inspect.getmembers(funs, inspect.isfunction)]
