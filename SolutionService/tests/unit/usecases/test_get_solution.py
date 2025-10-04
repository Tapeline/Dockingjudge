import pytest

from solution_service.application.exceptions import MayNotAccessSolution
from solution_service.application.interactors.get_solution import GetSolution
from tests.unit.factory import (
    UserFactory,
    QuizSolutionFactory,
)
from tests.unit.fakes import (
    FakeSolutionRepository, FakeUserIdP,
    FakeContestService,
)


@pytest.mark.asyncio
async def test_happy_path(
    fake_solution_repo: FakeSolutionRepository,
    get_solution_interactor: GetSolution,
    fake_user_idp: FakeUserIdP,
    user_factory: UserFactory,
    quiz_solution_factory: QuizSolutionFactory,
):
    user = user_factory.build()
    fake_user_idp.user = user
    solution = quiz_solution_factory.build(user_id=user.id)
    await fake_solution_repo.create_solution(solution)

    got_solution = await get_solution_interactor(solution.uid)

    assert got_solution == solution


@pytest.mark.asyncio
async def test_cannot_view_others_solutions(
    fake_solution_repo: FakeSolutionRepository,
    get_solution_interactor: GetSolution,
    fake_user_idp: FakeUserIdP,
    user_factory: UserFactory,
    quiz_solution_factory: QuizSolutionFactory,
):
    user = user_factory.build()
    other_user = user_factory.build()
    fake_user_idp.user = user
    solution = quiz_solution_factory.build(user_id=other_user.id)
    await fake_solution_repo.create_solution(solution)

    with pytest.raises(MayNotAccessSolution):
        await get_solution_interactor(solution.uid)


@pytest.mark.asyncio
async def test_can_view_others_solutions_if_manager(
    fake_solution_repo: FakeSolutionRepository,
    get_solution_interactor: GetSolution,
    fake_user_idp: FakeUserIdP,
    fake_contest_service: FakeContestService,
    user_factory: UserFactory,
    quiz_solution_factory: QuizSolutionFactory,
):
    user = user_factory.build()
    other_user = user_factory.build()
    fake_user_idp.user = user
    solution = quiz_solution_factory.build(user_id=other_user.id)
    await fake_solution_repo.create_solution(solution)
    fake_contest_service.contest_managers[solution.contest_id] = [user.id]

    got_solution = await get_solution_interactor(solution.uid)

    assert got_solution == solution
