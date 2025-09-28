import pytest

from judgelet.domain.test_group import TestGroup
from tests.unit.factory import create_group, create_suite, create_test
from tests.unit.fakes import (
    FakeOkValidator,
    FakeWrongAnswerValidator,
    create_fake_empty_runner,
)


@pytest.mark.parametrize(
    ("groups", "expected_total"),
    [
        ([
            create_group(
                "A",
                create_test(FakeOkValidator()),
                score=50,
            ),
            create_group(
                "B",
                create_test(FakeOkValidator()),
                score=50,
            ),
        ], 100),
        ([
            create_group(
                "A",
                create_test(FakeOkValidator()),
                score=50,
            ),
            create_group(
                "B",
                create_test(FakeWrongAnswerValidator()),
                score=50,
            ),
        ], 50)
    ]
)
@pytest.mark.asyncio
async def test_simple_group_score_sum(
    groups: list[TestGroup], expected_total: int
):
    test_suite = create_suite(*groups)
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.score == expected_total


@pytest.mark.parametrize(
    ("groups", "expected_total", "expected_group_scores"),
    [
        ([
            create_group(
                "A",
                create_test(FakeOkValidator()),
                score=50,
            ),
            create_group(
                "B",
                create_test(FakeOkValidator()),
                score=50,
            ),
        ], 100, {"A": 50, "B": 50}),
        ([
            create_group(
                "A",
                create_test(FakeOkValidator()),
                score=50,
            ),
            create_group(
                "B",
                create_test(FakeWrongAnswerValidator()),
                score=50,
            ),
        ], 50, {"A": 50, "B": 0}),
        ([
            create_group(
                "A",
                create_test(FakeWrongAnswerValidator()),
                score=50,
            ),
            create_group(
                "B",
                create_test(FakeOkValidator()),
                score=50,
            ),
        ], 0, {"A": 0})
    ]
)
@pytest.mark.asyncio
async def test_dependent_groups(
    groups: list[TestGroup],
    expected_total: int,
    expected_group_scores: dict[str, int]
):
    group_deps = {"B": ["A"]}
    test_suite = create_suite(*groups, group_deps=group_deps)
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.score == expected_total
    assert result.group_scores == expected_group_scores
