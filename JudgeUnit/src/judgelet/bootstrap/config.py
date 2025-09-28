import argparse

from adaptix import P
from fuente import config_loader
from fuente.sources.yaml import YamlSource
from fuente.sources.argparse import ArgParseSource
from fuente.sources.env import EnvSource
from fuente.merger_provider import merge
from fuente.merger.simple import UseFirst

from judgelet.config import Config

judgelet_config_loader = config_loader(
    EnvSource(prefix="JUDGELET_"),
    YamlSource("judgelet.yml"),
    recipe=[
        merge(P[Config].debug_mode, UseFirst()),
        merge(P[Config].enable_lock, UseFirst()),
    ],
    config=Config,
)


def load_config() -> Config:
    return judgelet_config_loader.load()
