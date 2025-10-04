from typing import Final

import pytest

from solution_service.domain.quiz_checkers import (
    QuizTextRegexChecker,
    QuizTextRegexCheckerParams,
)

CASE_SENSITIVE: Final = True  # Alias
STRICT: Final = True  # Alias


@pytest.mark.parametrize(
    ("expected_answer", "actual_answer"),
    [
        ("Apple", "Apple"),
        ("(A|a)pple", "apple"),
        ("app+le", "apple"),
    ],
)
def test_right_answers(
    expected_answer,
    actual_answer,
):
    checker = QuizTextRegexChecker(
        max_score=100,
        parameters=QuizTextRegexCheckerParams(
            pattern=expected_answer,
        ),
    )
    verdict = checker.check(actual_answer)
    assert verdict.is_successful


@pytest.mark.parametrize(
    ("expected_answer", "actual_answer"),
    [
        ("Apple", "apple"),
        ("(A|a)pple", "Aapple"),
        ("app+le", "aple"),
    ],
)
def test_wrong_answers(
    expected_answer,
    actual_answer,
):
    checker = QuizTextRegexChecker(
        max_score=100,
        parameters=QuizTextRegexCheckerParams(
            pattern=expected_answer,
        ),
    )
    verdict = checker.check(actual_answer)
    assert not verdict.is_successful
