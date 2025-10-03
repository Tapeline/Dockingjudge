from adaptix import P
from fuente import config_loader
from fuente.merger.simple import UseFirst
from fuente.merger_provider import merge
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from solution_service.config import Config

service_config_loader = config_loader(
    EnvSource(prefix="SOLUTION_SVC_", sep="__"),
    YamlSource("solution_service.yml"),
    config=Config,
)
