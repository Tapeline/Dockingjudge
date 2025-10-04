from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from solution_service.config import Config

service_config_loader = config_loader(
    EnvSource(prefix="SOLUTION_SVC_", sep="__"),
    YamlSource("solution_service.yml"),
    config=Config,
)
