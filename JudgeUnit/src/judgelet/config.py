import os

from pydantic import Field, BaseModel


class ModeConfig(BaseModel):
    debug_mode: bool = Field(alias="DEBUG", default=True)


class Config(BaseModel):
    mode: ModeConfig = Field(
        default_factory=lambda: ModeConfig(**os.environ)
    )
