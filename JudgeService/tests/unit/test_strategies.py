import pytest

from judgeservice.domain.pool.strategies import (
    RoundRobinBalancingStrategy,
    SingleBalancedStrategy, LeastConnectionsBalancingStrategy,
)
from tests.unit.factory import create_judgelets
from tests.unit.factory import create_simple_pool


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
        ]
    ]
)
@pytest.mark.asyncio
async def test_single_node_strategy(judgelets):
    pool = create_simple_pool(
        create_judgelets(judgelets),
        strategy=SingleBalancedStrategy(),
    )
    judgelet = await pool.get_for_compiler("does not matter")
    assert judgelet.address == "a"


@pytest.mark.asyncio
async def test_round_robin_strategy():
    pool = create_simple_pool(
        create_judgelets([
            {"address": "a"},
            {"address": "b"},
            {"address": "c"},
        ]),
        strategy=RoundRobinBalancingStrategy(),
    )
    await pool.get_for_compiler("does not matter")
    await pool.get_for_compiler("does not matter")
    third = await pool.get_for_compiler("does not matter")
    assert third.address == "c"


@pytest.mark.asyncio
async def test_least_connections_strategy():
    judgelets = create_judgelets([
        {"address": "a"},
        {"address": "b"},
        {"address": "c"},
    ])
    pool = create_simple_pool(
        judgelets,
        strategy=LeastConnectionsBalancingStrategy(),
    )
    # A has 2 connections
    judgelets[0].notify_opened_connection()
    judgelets[0].notify_opened_connection()
    # B has 1 connection
    judgelets[1].notify_opened_connection()
    # C has no connections, so choose it
    judgelets[2].notify_closed_connection()
    third = await pool.get_for_compiler("does not matter")
    assert third.address == "c"
