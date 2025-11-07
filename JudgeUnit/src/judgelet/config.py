from enum import StrEnum

from dataclasses import dataclass


class SandboxType(StrEnum):
    SIMPLE = "simple"
    BUBBLEWRAP = "bubblewrap"


@dataclass
class Config:
    """
    Judgelet config.

    Args:
        debug_mode: run in debug or release mode.
        enable_lock: if set to True, then only one solution at a time
            could be executed on this judgelet.
        sandbox: what sandbox type to use.
    """

    debug_mode: bool = True
    enable_lock: bool = True
    sandbox: SandboxType = SandboxType.SIMPLE
