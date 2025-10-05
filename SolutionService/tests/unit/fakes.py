import uuid
from collections.abc import Callable, Sequence
from typing import Any

from solution_service.application.exceptions import NotAuthenticated
from solution_service.application.interfaces.account import User
from solution_service.application.interfaces.contest import (
    AnyTaskDTO,
    CodeTaskDTO,
    ContestService,
    ContestTaskHead,
    QuizTaskDTO,
)
from solution_service.application.interfaces.publisher import SolutionPublisher
from solution_service.application.interfaces.solutions import (
    PaginationParameters,
    SolutionRepository,
    UserStandingRow,
)
from solution_service.application.interfaces.storage import (
    URL,
    DBSession,
    File,
    Storage,
)
from solution_service.application.interfaces.user import UserIdProvider
from solution_service.domain.abstract import (
    AnySolution,
    CodeSolution,
    TaskType,
)


class FakeSolutionRepository(SolutionRepository):
    def __init__(self):
        self.solutions: dict[str, AnySolution] = {}

    def _paginate(
        self,
        collection: list[AnySolution],
        params: PaginationParameters | None,
    ) -> list[AnySolution]:
        params = params or PaginationParameters()
        offset = params.offset or 0
        limit = params.limit or len(collection)
        return collection[offset:offset + limit]

    def _get_solutions_filtered_paginated(
        self,
        pagination: PaginationParameters | None,
        predicate: Callable[[AnySolution], bool],
    ) -> list[AnySolution]:
        return self._paginate(
            [
                solution for solution in self.solutions.values()
                if predicate(solution)
            ],
            pagination,
        )

    async def get_all_solutions_of_user(
        self,
        user_id: int,
        task_type: TaskType | None = None,
        pagination_params: PaginationParameters | None = None,
    ) -> list[AnySolution]:
        return self._get_solutions_filtered_paginated(
            pagination_params,
            lambda solution: (
                (
                    not task_type or solution.task_type == task_type
                ) and solution.user_id == user_id
            ),
        )

    async def get_all_solutions_of_task(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
        pagination_params: PaginationParameters | None = None,
    ) -> list[AnySolution]:
        return self._get_solutions_filtered_paginated(
            pagination_params,
            lambda solution:
            solution.task_type == task_type
            and solution.task_id == task_id
            and solution.user_id == user_id,
        )

    async def get_all_solutions_of_user_for_contest(
        self,
        user_id: int,
        contest_tasks: Sequence[tuple[TaskType, int]],
        pagination_params: PaginationParameters | None = None,
    ) -> Sequence[AnySolution]:
        return self._get_solutions_filtered_paginated(
            pagination_params,
            lambda solution:
            (solution.task_type, solution.task_id) in contest_tasks,
        )

    async def get_contest_standings(
        self,
        contest_tasks: Sequence[tuple[TaskType, int]],
        participants: Sequence[int],
    ) -> Sequence[UserStandingRow]:
        pass

    async def get_solution(self, solution_id: str) -> AnySolution | None:
        return self.solutions.get(solution_id, None)

    async def get_best_solution_by_user_task(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
    ) -> AnySolution | None:
        solutions = sorted(
            self._get_solutions_filtered_paginated(
                None,
                lambda solution:
                solution.task_type == task_type
                and solution.task_id == task_id
                and solution.user_id == user_id,
            ), key=lambda solution: solution.score,
        )
        if not solutions:
            return None
        return solutions[-1]

    async def create_solution(self, solution: AnySolution) -> None:
        self.solutions[solution.uid] = solution

    async def store_solution_check_result(
        self,
        solution_id: str,
        score: int,
        detailed_verdict: str,
        short_verdict: str,
        group_scores: dict[str, int],
        protocol: dict[str, Any],
    ) -> None:
        self.solutions[solution_id].score = score
        self.solutions[solution_id].detailed_verdict = detailed_verdict
        self.solutions[solution_id].short_verdict = short_verdict
        self.solutions[solution_id].group_scores = group_scores

    async def purge_user_solutions(self, user_id: int) -> None:
        for solution_id, solution in self.solutions.items():
            if solution.user_id == user_id:
                self.solutions.pop(solution_id)

    async def purge_task_solutions(
        self,
        task_type: TaskType,
        task_id: int,
    ) -> None:
        for solution_id, solution in self.solutions.items():
            if solution.task_id == task_id and solution.task_type == task_type:
                self.solutions.pop(solution_id)

    def place_solutions(self, *solutions: AnySolution) -> None:
        for solution in solutions:
            self.solutions[solution.uid] = solution


class FakeUserIdP(UserIdProvider):
    def __init__(self):
        self.user: User | None = None

    async def get_user(self) -> User | None:
        return self.user

    async def require_user(self) -> User:
        if not self.user:
            raise NotAuthenticated
        return self.user


class FakeContestService(ContestService):
    def __init__(self):
        self.contest_managers: dict[int, list[int]] = {}
        self.contest_tasks: dict[int, list[ContestTaskHead]] = {}
        self.contest_participants: dict[int, list[int]] = {}
        self.can_submit_task = True
        self.quiz_tasks: dict[int, QuizTaskDTO] = {}
        self.code_tasks: dict[int, CodeTaskDTO] = {}

    async def get_contest_managers(self, contest_id: int) -> Sequence[int]:
        return self.contest_managers.get(contest_id, [])

    async def get_contest_tasks(
        self, contest_id: int,
    ) -> Sequence[ContestTaskHead]:
        return self.contest_tasks.get(contest_id, [])

    async def get_contest_participants(self, contest_id: int) -> Sequence[int]:
        return self.contest_participants.get(contest_id, [])

    async def can_submit(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
    ) -> bool:
        return self.can_submit_task

    async def get_task(
        self,
        task_type: str,
        task_id: int,
    ) -> AnyTaskDTO | None:
        if task_type.lower() == "quiz":
            return await self.get_quiz_task(task_id)
        if task_type.lower() == "code":
            return await self.get_code_task(task_id)
        raise AssertionError("unknown task type")

    async def get_quiz_task(self, task_id: int) -> QuizTaskDTO | None:
        return self.quiz_tasks.get(task_id, None)

    async def get_code_task(self, task_id: int) -> CodeTaskDTO | None:
        return self.code_tasks.get(task_id, None)


class FakeObjectStore(Storage):
    def __init__(self) -> None:
        self.files = {}
        self.filenames_to_uids = {}

    async def get_file_url(self, name: str) -> URL:
        if name not in self.filenames_to_uids:
            self.filenames_to_uids[name] = f"fake_s3://{uuid.uuid4()}"
        return self.filenames_to_uids[name]

    async def save_file(self, file: File) -> URL:
        url = await self.get_file_url(file.name)
        self.files[url] = file
        return url

    async def get_file(self, url: URL) -> File:
        return self.files[url]


class FakeSolutionPublisher(SolutionPublisher):
    def __init__(self) -> None:
        self.published = []

    async def publish(
        self, solution: CodeSolution, test_suite: dict[str, Any],
    ) -> None:
        self.published.append((solution, test_suite))


class FakeDBSession(DBSession):
    async def commit(self) -> None:
        ...

    async def flush(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
