import inspect

import funs

__all__ = {n: obj for n, obj in inspect.getmembers(funs, inspect.isfunction)}
