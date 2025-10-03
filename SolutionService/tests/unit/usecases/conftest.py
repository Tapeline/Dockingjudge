import pytest

from solution_service.application.interactors.get_solution import GetSolution
from solution_service.application.interfaces.solutions import (
    SolutionRepository
)
from solution_service.application.interfaces.user import UserIdProvider
from tests.unit.fakes import FakeSolutionRepository, FakeUserIdP


@pytest.fixture
def fake_solution_repo() -> FakeSolutionRepository:
    return FakeSolutionRepository()


@pytest.fixture
def fake_user_idp() -> FakeUserIdP:
    return FakeUserIdP()


@pytest.fixture
def get_solution_interactor(
    fake_solution_repo: SolutionRepository,
    fake_user_idp: UserIdProvider,
    fake_contest_service:
) -> GetSolution:
    return GetSolution(
        solution_repository=fake_solution_repo,
        user_idp=fake_user_idp,
        contest_service=
    )