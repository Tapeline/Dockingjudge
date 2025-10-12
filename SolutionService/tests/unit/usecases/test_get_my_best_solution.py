from typing import Any

import pytest

from solution_service.application.interactors.get_solution import (
    GetBestSolutionForUserOnTask,
)
from tests.unit.factory import (
    QuizSolutionFactory,
    UserFactory,
)
from tests.unit.fakes import (
    FakeSolutionRepository,
    FakeUserIdP,
)


@pytest.mark.parametrize(
    ("solution_params", "expected_n"),
    [
        ([], None),
        ([dict(score=0)], 0),
        ([dict(score=20)], 0),
        ([dict(score=20), dict(score=40)], 1),
        ([dict(score=40), dict(score=40)], 1),
        ([dict(score=40), dict(score=40), dict(score=40)], 2),
    ],
)
@pytest.mark.parametrize(
    ("task_id", "task_type"), [(1, "quiz")],
)
@pytest.mark.asyncio
async def test_best_solution(
    fake_solution_repo: FakeSolutionRepository,
    get_my_best_solution_interactor: GetBestSolutionForUserOnTask,
    fake_user_idp: FakeUserIdP,
    user_factory: UserFactory,
    quiz_solution_factory: QuizSolutionFactory,
    task_id: int,
    task_type: str,
    solution_params: list[dict[str, Any]],
    expected_n: int,
):
    user = user_factory.build()
    fake_user_idp.user = user
    solutions = [
        quiz_solution_factory.build(
            user_id=user.id,
            task_id=task_id,
            **params,
        )
        for params in solution_params
    ]
    fake_solution_repo.place_solutions(*solutions)

    got_solution = await get_my_best_solution_interactor(task_type, task_id)

    if expected_n is None:
        assert got_solution is None
    else:
        assert got_solution == solutions[expected_n]
