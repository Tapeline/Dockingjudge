from typing import overload

from solution_service.controllers.schemas import (
    CodeSolutionExtraSchema,
    QuizSolutionExtraSchema,
    SolutionSchema,
)
from solution_service.domain.abstract import AnySolution, TaskType


@overload
def serialize_solution(
    solution: AnySolution, *,
    is_safe: bool = False,
) -> SolutionSchema: ...


@overload
def serialize_solution(
    solution: None, *,
    is_safe: bool = False,
) -> None: ...


def serialize_solution(
    solution: AnySolution | None, *,
    is_safe: bool = False,
) -> SolutionSchema | None:
    """Serialize solution DM into solution response model."""
    if not solution:
        return None
    data = None
    if not is_safe and solution.task_type == TaskType.QUIZ:
        data = QuizSolutionExtraSchema(
            submitted_answer=solution.submitted_answer,
        )
    if not is_safe and solution.task_type == TaskType.CODE:
        data = CodeSolutionExtraSchema(
            compiler=solution.compiler_name,
            submission_url=solution.submission_url,
            group_scores=solution.group_scores,
            detailed_verdict=solution.detailed_verdict,
        )
    return SolutionSchema(
        id=solution.uid,
        task_id=solution.task_id,
        task_type=solution.task_type,
        user_id=solution.user_id,
        score=solution.score,
        short_verdict=solution.short_verdict,
        submitted_at=solution.submitted_at,
        data=data,
    )
