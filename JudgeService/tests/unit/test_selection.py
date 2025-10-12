import pytest

from judgeservice.domain.exceptions import NoSuitableJudgeletFoundException
from judgeservice.domain.pool.strategies import (
    LeastConnectionsBalancingStrategy,
    RoundRobinBalancingStrategy,
)
from tests.unit.factory import (
    create_judgelets,
    create_multigroup_pool,
    create_simple_pool,
)


@pytest.mark.parametrize(
    "judgelets",
    [
        [
            {"address": "a"},
        ],
        [
            {"address": "a"},
            {"address": "b"},
            {"address": "c"},
        ],
    ],
)
@pytest.mark.asyncio
async def test_single_group_selected(judgelets):
    pool = create_simple_pool(create_judgelets(judgelets))
    judgelet = await pool.get_for_compiler("does not matter")
    assert judgelet.address == "a"


@pytest.mark.parametrize(
    "judgelets",
    [
        [
            {"address": "a", "is_alive": False},
            {"address": "b"},
        ],
    ],
)
@pytest.mark.asyncio
async def test_healthy_selected(judgelets):
    pool = create_simple_pool(create_judgelets(judgelets))
    judgelet = await pool.get_for_compiler("does not matter")
    assert judgelet.address == "b"


@pytest.mark.parametrize(
    "judgelets",
    [
        [
            {"address": "a", "is_alive": False},
            {"address": "b", "is_alive": False},
        ],
    ],
)
@pytest.mark.parametrize(
    "strategy",
    [
        RoundRobinBalancingStrategy(),
        LeastConnectionsBalancingStrategy(),
    ],
)
@pytest.mark.asyncio
async def test_no_healthy_found(judgelets, strategy):
    pool = create_simple_pool(create_judgelets(judgelets), strategy=strategy)
    with pytest.raises(NoSuitableJudgeletFoundException):
        await pool.get_for_compiler("does not matter")


@pytest.mark.parametrize(
    "groups",
    [
        [
            ("compiler_b", {"address": "should be selected"}),
            ("compiler_a", {"address": "should not be selected"}),
        ],
        [
            ("compiler_a", {"address": "should not be selected"}),
            ("compiler_b", {"address": "should be selected"}),
        ],
        [
            ("*", {"address": "should be selected"}),
            ("compiler_b", {"address": "should not be selected"}),
        ],
    ],
)
@pytest.mark.asyncio
async def test_multigroup_selected(groups):
    pool = create_multigroup_pool(*groups)
    judgelet = await pool.get_for_compiler("compiler_b")
    assert judgelet.address == "should be selected"


@pytest.mark.parametrize(
    "groups",
    [
        [
            ("compiler_a", {"address": "should not be selected"}),
            ("compiler_b", {"address": "should not be selected"}),
        ],
    ],
)
@pytest.mark.asyncio
async def test_no_group_selected(groups):
    pool = create_multigroup_pool(*groups)
    with pytest.raises(NoSuitableJudgeletFoundException):
        await pool.get_for_compiler("compiler_c")


@pytest.mark.parametrize(
    "strategy",
    [
        RoundRobinBalancingStrategy(),
        LeastConnectionsBalancingStrategy(),
    ],
)
@pytest.mark.asyncio
async def test_no_groups_configured(strategy):
    # no groups configured
    pool = create_multigroup_pool(strategy=strategy)
    with pytest.raises(NoSuitableJudgeletFoundException):
        await pool.get_for_compiler("does not matter")
