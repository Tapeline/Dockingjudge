from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from solution_service.config import Config

service_config_loader = config_loader(
    YamlSource("solution_service.yml"),
    EnvSource(prefix="SOLUTION_SVC_", sep="__"),
    config=Config,
)
