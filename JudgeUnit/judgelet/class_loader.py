"""Utils for DI"""

import importlib


def load_class(name: str, subclass_constraint):
    """Load class by name"""
    attr = name[name.rfind(".") + 1:]
    name = name[:name.rfind(".")]
    module = importlib.import_module(name)
    cls = getattr(module, attr)
    if not issubclass(cls, subclass_constraint):
        raise TypeError(f"Subclass constraint failed on {cls}. Expected {subclass_constraint}")
    return cls
