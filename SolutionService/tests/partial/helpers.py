import asyncio
import uuid
from typing import Any

from solution_service.application.interfaces.solutions import (
    UserSolutionScore,
    UserStandingRow,
)
from solution_service.domain.abstract import QuizSolution, TaskType
from solution_service.infrastructure.persistence.repo_impl import (
    SolutionRepoImpl,
)


def row(
    *scores: tuple[int, int] | None,
    user_id: int,
    attempted: int,
    solved: int,
    total: int,
) -> UserStandingRow:
    return UserStandingRow(
        total_score=total,
        tasks_attempted=attempted,
        tasks_solved=solved,
        solutions=[
            UserSolutionScore(
                user_id=user_id,
                task_type=TaskType.QUIZ,
                task_id=score[0],
                score=score[1],
                short_verdict="OK" if score[1] == 100 else "WA"
            ) if score else None
            for score in scores
        ],
    )


def solution(
    score: int, task_id: int, user_id: int,
) -> dict[str, Any]:
    return {
        "score": score,
        "task_id": task_id,
        "user_id": user_id,
        "short_verdict": "OK" if score == 100 else "WA",
    }


def solution_factory(params: dict[str, Any]) -> QuizSolution:
    return QuizSolution(
        **(dict(
            uid=str(uuid.uuid4()),
            contest_id=1,
            task_id=1,
            task_type=TaskType.QUIZ,
            user_id=1,
            score=100,
            short_verdict="OK",
            submitted_answer="ans",
        ) | params),
    )


async def create_solutions(
    solutions: list[QuizSolution],
    solution_repo: SolutionRepoImpl,
) -> None:
    await asyncio.gather(
        *(
            solution_repo.create_solution(solution)
            for solution in solutions
        ),
    )
