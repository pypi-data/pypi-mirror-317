from __future__ import absolute_import


from stensor.ops import functional
from stensor.ops.functional import *

__all__ = []
# Expose API which defined only in functional.py
with open(functional.__file__, 'r') as f:  
    import inspect
    for name, val in inspect.getmembers(functional, inspect.isfunction):
        if val.__module__ == functional.__name__:
            __all__.append(name)
