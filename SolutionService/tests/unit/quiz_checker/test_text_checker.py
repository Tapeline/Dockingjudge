from typing import Final

import pytest

from solution_service.domain.quiz_checkers import QuizTextChecker, QuizTextCheckerParams


CASE_SENSITIVE: Final = True  # Alias
STRICT: Final = True  # Alias


@pytest.mark.parametrize(
    ("expected_answer", "actual_answer", "is_case_sensitive", "is_strict"),
    [
        ("Apple", "Apple", CASE_SENSITIVE, STRICT),
        ("Apple", "aPPlE", not CASE_SENSITIVE, STRICT),
        ("Apple", "Aple", ..., not STRICT)
    ]
)
def test_right_answers(
    expected_answer,
    actual_answer,
    is_case_sensitive,
    is_strict
):
    checker = QuizTextChecker(
        max_score=100,
        parameters=QuizTextCheckerParams(
            case_insensitive=not is_case_sensitive,
            strict_match=is_strict,
            pattern=expected_answer,
        ),
    )
    verdict = checker.check(actual_answer)
    if is_strict:
        assert verdict.score == 100
        assert verdict.is_successful
    else:
        assert verdict.score > 0


@pytest.mark.parametrize(
    ("expected_answer", "actual_answer", "is_case_sensitive", "is_strict"),
    [
        ("Apple", "apple", CASE_SENSITIVE, STRICT),
        ("Apple", "aple", not CASE_SENSITIVE, STRICT),
    ]
)
def test_wrong_answers(
    expected_answer,
    actual_answer,
    is_case_sensitive,
    is_strict
):
    checker = QuizTextChecker(
        max_score=100,
        parameters=QuizTextCheckerParams(
            case_insensitive=not is_case_sensitive,
            strict_match=is_strict,
            pattern=expected_answer,
        ),
    )
    verdict = checker.check(actual_answer)
    assert not verdict.is_successful
