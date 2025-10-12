import pytest

from judgelet.config import Config


@pytest.fixture
def test_config() -> Config:
    return Config(
        debug_mode=True,
        enable_lock=False,
    )
