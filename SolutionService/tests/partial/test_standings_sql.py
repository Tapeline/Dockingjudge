import asyncio
import sqlite3
import uuid
from typing import Any

import pytest

from solution_service.application.interfaces.solutions import (
    UserStandingRow,
    UserSolutionScore,
)
from solution_service.domain.abstract import QuizSolution, TaskType
from solution_service.infrastructure.persistence.repo_impl import \
    SolutionRepoImpl
from tests.partial.helpers import (
    solution, row, solution_factory,
    create_solutions,
)


@pytest.mark.parametrize(
    ("solutions_params", "contest_tasks", "participants", "expected"),
    [
        (
            [
                solution(100, task_id=1, user_id=1),
                solution(100, task_id=2, user_id=1),
                solution(0, task_id=3, user_id=1),
            ],
            [1, 2, 3],
            [1],
            [
                row(
                    (1, 100),
                    (2, 100),
                    (3, 0),
                    user_id=1,
                    attempted=3,
                    solved=2,
                    total=200,
                ),
            ]
        ),
        # multiple users
        (
            [
                solution(100, task_id=1, user_id=1),
                solution(50, task_id=2, user_id=1),
                solution(100, task_id=1, user_id=2),
                solution(100, task_id=2, user_id=2),
            ],
            [1, 2],
            [1, 2],
            [
                row(
                    (1, 100),
                    (2, 50),
                    user_id=1,
                    attempted=2,
                    solved=1,
                    total=150,
                ),
                row(
                    (1, 100),
                    (2, 100),
                    user_id=2,
                    attempted=2,
                    solved=2,
                    total=200,
                ),
            ]
        ),
        # user with no solutions
        (
            [
                solution(100, task_id=1, user_id=1),
            ],
            [1],
            [1, 2],
            [
                row(
                    (1, 100),
                    user_id=1,
                    attempted=1,
                    solved=1,
                    total=100,
                ),
                row(
                    None,
                    user_id=2,
                    attempted=0,
                    solved=0,
                    total=0,
                ),
            ]
        ),
        # solutions from other contests (tasks not in contest_tasks)
        (
            [
                solution(100, task_id=1, user_id=1),
                solution(100, task_id=99, user_id=1),
            ],
            [1, 2],
            [1],
            [
                row(
                    (1, 100),
                    None,
                    user_id=1,
                    attempted=1,
                    solved=1,
                    total=100,
                ),
            ]
        ),
        # multiple attempts on the same task, only best counts
        (
            [
                solution(50, task_id=1, user_id=1),
                solution(100, task_id=1, user_id=1),
                solution(75, task_id=1, user_id=1),
            ],
            [1],
            [1],
            [
                row(
                    (1, 100),
                    user_id=1,
                    attempted=1,
                    solved=1,
                    total=100,
                ),
            ]
        ),
        # multiple solutions with the same max score
        (
            [
                solution(100, task_id=1, user_id=1),
                solution(100, task_id=1, user_id=1),
            ],
            [1],
            [1],
            [
                row(
                    (1, 100),
                    user_id=1,
                    attempted=1,
                    solved=1,
                    total=100,
                ),
            ]
        ),
        # empty participants list
        (
            [
                solution(100, task_id=1, user_id=1),
            ],
            [1],
            [],
            []
        ),
        # empty contest_tasks list
        (
            [
                solution(100, task_id=1, user_id=1),
            ],
            [],
            [1],
            [
                row(
                    user_id=1,
                    attempted=0,
                    solved=0,
                    total=0,
                ),
            ]
        ),
        # user with solutions but not in participants list
        (
            [
                solution(100, task_id=1, user_id=1),
                solution(100, task_id=1, user_id=2),
            ],
            [1],
            [1],
            [
                row(
                    (1, 100),
                    user_id=1,
                    attempted=1,
                    solved=1,
                    total=100,
                ),
            ]
        ),
        # participant order is preserved
        (
            [
                solution(100, task_id=1, user_id=1),
                solution(50, task_id=1, user_id=2),
            ],
            [1],
            [2, 1],
            [
                row(
                    (1, 50),
                    user_id=2,
                    attempted=1,
                    solved=0,
                    total=50,
                ),
                row(
                    (1, 100),
                    user_id=1,
                    attempted=1,
                    solved=1,
                    total=100,
                ),
            ]
        ),
    ]
)
@pytest.mark.asyncio
async def test_standings(
    sqlite_base: sqlite3.Connection,
    solution_repo: SolutionRepoImpl,
    solutions_params: list[dict[str, Any]],
    contest_tasks: list[int],
    participants: list[int],
    expected: list[UserStandingRow]
):
    solutions = list(map(solution_factory, solutions_params))
    await create_solutions(solutions, solution_repo)
    result = await solution_repo.get_contest_standings(
        [(TaskType.QUIZ, task_id) for task_id in contest_tasks],
        participants,
    )
    assert result == expected
