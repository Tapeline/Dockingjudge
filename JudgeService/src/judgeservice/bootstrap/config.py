from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from judgeservice.bootstrap.exceptions import BadBalancingStrategy
from judgeservice.config import Config
from judgeservice.infrastructure.pool.judgelet import JudgeletImpl
from judgeservice.infrastructure.pool.pool import (
    JudgeletGroup,
    JudgeletPoolImpl,
    Selector,
)
from judgeservice.infrastructure.pool.strategies import (
    STRATEGIES,
    AbstractBalancingStrategy,
    SingleBalancedStrategy,
)

service_config_loader = config_loader(
    EnvSource(prefix="JUDGE_SVC_"),
    YamlSource("config.yml"),
    config=Config,
)


def load_pool_impl(config: Config) -> JudgeletPoolImpl:
    """Load pool implementation from config."""
    strategy = _get_load_balancer(config.pool.load_balancing)
    return JudgeletPoolImpl(
        balancing_strategy=strategy,
        groups=[
            JudgeletGroup(
                selector=Selector(group.selector),
                nodes=(
                    [JudgeletImpl(addr, config) for addr in group.nodes]
                    if isinstance(group.nodes, list)
                    else [JudgeletImpl(group.nodes, config)]
                ),
            )
            for group in config.pool.groups
        ],
    )


def _get_load_balancer(name: str | None) -> AbstractBalancingStrategy:
    if name is None:
        return SingleBalancedStrategy()
    if name not in STRATEGIES:
        raise BadBalancingStrategy(f"No strategy with name {name}")
    return STRATEGIES[name]()
