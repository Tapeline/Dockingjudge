import pytest

from judgelet.application.scoring_poilicies import (
    GradualScoringPolicy,
    PolarScoringPolicy,
)
from judgelet.domain.test_case import TestCase
from tests.unit.factory import create_group, create_suite, create_test
from tests.unit.fakes import (
    FakeOkValidator,
    FakePresentErrorValidator,
    FakeWrongAnswerValidator,
    create_fake_empty_runner,
)


@pytest.mark.parametrize(
    ("tests", "expected_score"),
    [
        ([
             create_test(FakeOkValidator())
         ], 100),
        ([
             create_test(FakeOkValidator()),
             create_test(FakeOkValidator())
         ], 100),
        ([
             create_test(FakeOkValidator()),
             create_test(FakeWrongAnswerValidator())
         ], 50),
        ([
             create_test(FakeOkValidator()),
             create_test(FakeOkValidator()),
             create_test(FakeOkValidator()),
             create_test(FakeWrongAnswerValidator())
         ], 75),
    ]
)
@pytest.mark.asyncio
async def test_gradual_scoring_policy(
    tests: list[TestCase],
    expected_score: int
):
    test_suite = create_suite(
        create_group("A", *tests, scoring_policy=GradualScoringPolicy())
    )
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.score == expected_score


@pytest.mark.parametrize(
    ("tests", "expected_score"),
    [
        ([
             create_test(FakeOkValidator())
         ], 100),
        ([
             create_test(FakeOkValidator()),
             create_test(FakeOkValidator())
         ], 100),
        ([
             create_test(FakeOkValidator()),
             create_test(FakeWrongAnswerValidator())
         ], 0),
        ([
             create_test(FakeOkValidator()),
             create_test(FakeOkValidator()),
             create_test(FakeOkValidator()),
             create_test(FakeWrongAnswerValidator())
         ], 0),
    ]
)
@pytest.mark.asyncio
async def test_polar_scoring_policy(
    tests: list[TestCase],
    expected_score: int
):
    test_suite = create_suite(
        create_group("A", *tests, scoring_policy=PolarScoringPolicy())
    )
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.score == expected_score
