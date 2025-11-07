from adaptix import P
from fuente import config_loader
from fuente.merger.simple import UseFirst
from fuente.merger_provider import merge
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from judgelet.config import Config

judgelet_config_loader = config_loader(
    YamlSource("judgelet.yml"),
    EnvSource(prefix="JUDGELET_"),
    config=Config,
)
