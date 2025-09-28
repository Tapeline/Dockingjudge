from judgelet.config import Config


def test_config() -> Config:
    return Config(
        debug_mode=True,
        enable_lock=False,
    )
