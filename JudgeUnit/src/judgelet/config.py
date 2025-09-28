from dataclasses import dataclass


@dataclass
class Config:
    debug_mode: bool = True
    enable_lock: bool = True
