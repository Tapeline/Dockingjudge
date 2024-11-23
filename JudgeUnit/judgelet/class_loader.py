"""Utils for DI"""

import importlib
import logging


def load_class(name: str, subclass_constraint):
    """Load class by name"""
    attr = name[name.rfind(".") + 1:]
    name = name[:name.rfind(".")]
    try:
        module = importlib.import_module(name)
        cls = getattr(module, attr)
    except (ImportError, AttributeError) as e:
        logging.error("Failed to obtain %s.%s", name, attr)
        raise e
    if not issubclass(cls, subclass_constraint):
        raise TypeError(f"Subclass constraint failed on {cls}. Expected {subclass_constraint}")
    return cls
