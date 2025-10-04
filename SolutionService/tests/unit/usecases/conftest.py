import pytest
from polyfactory.pytest_plugin import register_fixture

from solution_service.application.interactors.get_solution import (
    GetBestSolutionForUserOnTask,
    GetSolution,
)
from solution_service.application.interactors.post_code_solution import (
    PostCodeSolution,
)
from solution_service.application.interactors.post_quiz_solution import (
    PostQuizSolution,
)
from solution_service.config import (
    Config,
    MinioConfig,
    OuterServicesConfig,
    PostgresConfig,
    RabbitMQConfig,
)
from solution_service.infrastructure.persistence.id_gen import (
    DefaultUUIDGenerator,
)
from tests.unit.factory import (
    CodeSolutionFactory,
    CodeTaskFactory,
    NewCodeSolutionFactory,
    NewQuizSolutionFactory,
    QuizSolutionFactory,
    QuizTaskFactory,
    UserFactory,
)
from tests.unit.fakes import (
    FakeContestService,
    FakeObjectStore,
    FakeSolutionPublisher,
    FakeSolutionRepository,
    FakeUserIdP,
)


@pytest.fixture
def test_config() -> Config:
    return Config(
        rabbitmq=RabbitMQConfig(),
        encoding="utf-8",
        postgres=PostgresConfig(),
        services=OuterServicesConfig(),
        debug_mode=True,
        s3=MinioConfig(),
    )


@pytest.fixture
def fake_solution_repo() -> FakeSolutionRepository:
    return FakeSolutionRepository()


@pytest.fixture
def fake_user_idp() -> FakeUserIdP:
    return FakeUserIdP()


@pytest.fixture
def fake_contest_service() -> FakeContestService:
    return FakeContestService()


@pytest.fixture
def fake_object_store() -> FakeObjectStore:
    return FakeObjectStore()


@pytest.fixture
def fake_solution_publisher() -> FakeSolutionPublisher:
    return FakeSolutionPublisher()


@pytest.fixture
def get_solution_interactor(
    fake_solution_repo: FakeSolutionRepository,
    fake_user_idp: FakeUserIdP,
    fake_contest_service: FakeContestService,
) -> GetSolution:
    return GetSolution(
        solution_repository=fake_solution_repo,
        user_idp=fake_user_idp,
        contest_service=fake_contest_service,
    )


@pytest.fixture
def get_my_best_solution_interactor(
    fake_solution_repo: FakeSolutionRepository,
    fake_user_idp: FakeUserIdP,
) -> GetBestSolutionForUserOnTask:
    return GetBestSolutionForUserOnTask(
        solution_repository=fake_solution_repo,
        user_idp=fake_user_idp,
    )


@pytest.fixture
def post_code_solution_interactor(
    fake_solution_repo: FakeSolutionRepository,
    fake_user_idp: FakeUserIdP,
    fake_contest_service: FakeContestService,
    fake_solution_publisher: FakeSolutionPublisher,
    test_config: Config,
    fake_object_store: FakeObjectStore,
) -> PostCodeSolution:
    return PostCodeSolution(
        object_storage=fake_object_store,
        solutions=fake_solution_repo,
        contest_service=fake_contest_service,
        solution_publisher=fake_solution_publisher,
        config=test_config,
        user_idp=fake_user_idp,
        id_gen=DefaultUUIDGenerator(),
    )


@pytest.fixture
def post_quiz_solution_interactor(
    fake_solution_repo: FakeSolutionRepository,
    fake_user_idp: FakeUserIdP,
    fake_contest_service: FakeContestService,
    test_config: Config,
) -> PostQuizSolution:
    return PostQuizSolution(
        user_idp=fake_user_idp,
        solution_repository=fake_solution_repo,
        contest_service=fake_contest_service,
        id_gen=DefaultUUIDGenerator(),
        config=test_config,
    )


register_fixture(UserFactory)
register_fixture(QuizSolutionFactory)
register_fixture(CodeSolutionFactory)
register_fixture(NewCodeSolutionFactory)
register_fixture(CodeTaskFactory)
register_fixture(NewQuizSolutionFactory)
register_fixture(QuizTaskFactory)
