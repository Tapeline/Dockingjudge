"""Utils for DI"""

import importlib
import logging
from typing import Type


def load_class[T](name: str, subclass_constraint: Type[T]) -> Type[T]:
    """
    Load class by name.

    Args:
        name: fully qualified class name
        subclass_constraint: enforce class to be that subclass
    Raises:
        ImportError: target module cannot be found
        AttributeError: target class in module cannot be found
        TypeError: target class failed to fulfill defined subclass
                   constraint
    Returns:
        loaded class
    """
    attr = name[name.rfind(".") + 1:]
    name = name[:name.rfind(".")]
    try:  # noqa: WPS229 (too long try)
        module = importlib.import_module(name)
        target_class = getattr(module, attr)
    except ImportError as exception:
        logging.error("Failed to obtain module %s", name)
        raise exception
    except AttributeError as exception:
        logging.error("Failed to obtain class %s.%s", name, attr)
        raise exception

    if not issubclass(target_class, subclass_constraint):
        raise TypeError(
            f"Subclass constraint failed on {target_class}. "
            f"Expected {subclass_constraint}"
        )
    return target_class
