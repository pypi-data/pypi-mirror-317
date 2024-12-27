import inspect

import _funs

__all__ = {n: obj for n, obj in inspect.getmembers(_funs, inspect.isfunction)}
print(__all__)
