from dataclasses import dataclass


@dataclass
class Config:
    """
    Judgelet config.

    Args:
        debug_mode: run in debug or release mode.
        enable_lock: if set to True, then only one solution at a time
            could be executed on this judgelet.

    """

    debug_mode: bool = True
    enable_lock: bool = True
