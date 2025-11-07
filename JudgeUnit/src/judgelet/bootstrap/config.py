from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from judgelet.config import Config

judgelet_config_loader = config_loader(
    YamlSource("judgelet.yml"),
    EnvSource(prefix="JUDGELET_", sep="__"),
    config=Config,
)
