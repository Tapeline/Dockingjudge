from fuente import config_loader
from fuente.sources.env import EnvSource
from fuente.sources.yaml import YamlSource

from judgeservice.bootstrap.exceptions import BadBalancingStrategy
from judgeservice.config import Config
from judgeservice.domain.pool.pool import (
    JudgeletGroup,
    JudgeletPool,
    Selector,
)
from judgeservice.domain.pool.strategies import (
    STRATEGIES,
    AbstractBalancingStrategy,
    SingleBalancedStrategy,
)
from judgeservice.infrastructure.judgelet import JudgeletImpl

service_config_loader = config_loader(
    YamlSource("config.yml"),
    EnvSource(prefix="JUDGE_SVC_"),
    config=Config,
)


def load_pool_impl(config: Config) -> JudgeletPool:
    """Load pool implementation from config."""
    strategy = _get_load_balancer(config.pool.load_balancing)
    return JudgeletPool(
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
