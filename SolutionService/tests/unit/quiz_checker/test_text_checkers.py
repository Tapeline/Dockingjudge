import pytest

from solution_service.domain.entities.abstract import QuizSolution, TaskType
from solution_service.domain.entities.quiz_checkers import QuizTextChecker, QuizTextCheckerParams
from solution_service.domain.usecases.check import CheckQuizSolution


def _dummy_solution(answer: str) -> QuizSolution:
    return QuizSolution(
        uid="0000",
        task_id=1,
        user_id=1,
        score=0,
        short_verdict="NC",
        submitted_answer=answer,
        task_type=TaskType.QUIZ,
        contest_id=1,
    )


CASE_SENSITIVE = True  # Alias
STRICT = True  # Alias


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
    check = CheckQuizSolution(
        quiz_checker=QuizTextChecker(
            max_score=100,
            parameters=QuizTextCheckerParams(
                case_insensitive=not is_case_sensitive,
                strict_match=is_strict,
                pattern=expected_answer,
            ),
        )
    )
    verdict = check(_dummy_solution(actual_answer))
    if is_strict:
        assert verdict.score == 100
        assert verdict.is_successful
    else:
        assert verdict.score > 0
