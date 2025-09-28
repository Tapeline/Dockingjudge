import pytest

from judgelet.domain.test_case import TestCase
from tests.unit.factory import create_group, create_suite, create_test
from tests.unit.fakes import (
    FakeOkValidator,
    FakePresentErrorValidator,
    FakeWrongAnswerValidator,
    create_fake_empty_runner,
)


@pytest.mark.parametrize(
    "tests",
    [
        [
            create_test(FakeOkValidator())
        ],
        [
            create_test(FakeOkValidator()),
            create_test(FakeOkValidator())
        ]
    ]
)
@pytest.mark.asyncio
async def test_all_ok(tests: list[TestCase]):
    test_suite = create_suite(
        create_group("A", *tests)
    )
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.verdict.codename == "OK"
    assert result.score == 100


@pytest.mark.parametrize(
    "tests",
    [
        [
            create_test(FakeWrongAnswerValidator())
        ],
        [
            create_test(FakeOkValidator()),
            create_test(FakeWrongAnswerValidator())
        ],
        [
            create_test(FakeWrongAnswerValidator()),
            create_test(FakeOkValidator())
        ]
    ]
)
@pytest.mark.asyncio
async def test_wrong_answer(tests: list[TestCase]):
    test_suite = create_suite(
        create_group("A", *tests)
    )
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.verdict.codename == "WA"
    assert result.score != 100


@pytest.mark.parametrize(
    "tests",
    [
        [
            create_test(FakePresentErrorValidator())
        ],
        [
            create_test(FakeOkValidator()),
            create_test(FakePresentErrorValidator())
        ],
        [
            create_test(FakePresentErrorValidator()),
            create_test(FakeOkValidator())
        ]
    ]
)
@pytest.mark.asyncio
async def test_present_error(tests: list[TestCase]):
    test_suite = create_suite(
        create_group("A", *tests)
    )
    runner = create_fake_empty_runner()
    result = await test_suite.run(runner)
    assert result.verdict.codename == "PE"
    assert result.score != 100

