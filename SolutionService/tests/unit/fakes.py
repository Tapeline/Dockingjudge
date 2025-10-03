from collections.abc import Callable
from typing import Any, Sequence

from solution_service.application.exceptions import NotAuthenticated
from solution_service.application.interfaces.account import User
from solution_service.application.interfaces.contest import (
    AnyTaskDTO, CodeTaskDTO,
    ContestService, ContestTaskHead, QuizTaskDTO,
)
from solution_service.application.interfaces.solutions import (
    PaginationParameters, SolutionRepository, UserStandingRow,
)
from solution_service.application.interfaces.user import UserIdProvider
from solution_service.domain.abstract import AnySolution, TaskType


class FakeSolutionRepository(SolutionRepository):
    def __init__(self):
        self.solutions: dict[str, AnySolution] = {}

    def _paginate(
        self,
        collection: list[AnySolution],
        params: PaginationParameters | None
    ) -> list[AnySolution]:
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
            pagination
        )

    async def get_all_solutions_of_user(
        self,
        user_id: int,
        task_type: TaskType | None = None,
        pagination_params: PaginationParameters | None = None
    ) -> list[AnySolution]:
        return self._get_solutions_filtered_paginated(
            pagination_params,
            lambda solution: (
                                 not task_type or solution.task_type == task_type
                             ) and solution.user_id == user_id
        )

    async def get_all_solutions_of_task(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
        pagination_params: PaginationParameters | None = None
    ) -> list[AnySolution]:
        return self._get_solutions_filtered_paginated(
            pagination_params,
            lambda solution:
            solution.task_type == task_type
            and solution.task_id == task_id
            and solution.user_id == user_id
        )

    async def get_all_solutions_of_user_for_contest(
        self,
        user_id: int,
        contest_tasks: Sequence[tuple[TaskType, int]],
        pagination_params: PaginationParameters | None = None
    ) -> Sequence[AnySolution]:
        return self._get_solutions_filtered_paginated(
            pagination_params,
            lambda solution:
            (solution.task_type, solution.task_id) in contest_tasks
        )

    async def get_contest_standings(
        self,
        contest_tasks: Sequence[tuple[TaskType, int]],
        participants: Sequence[int]
    ) -> Sequence[UserStandingRow]:
        pass

    async def get_solution(self, solution_id: str) -> AnySolution | None:
        return self.solutions.get(solution_id, None)

    async def get_best_solution_by_user_task(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int
    ) -> AnySolution | None:
        solutions = self._get_solutions_filtered_paginated(
            None,
            lambda solution:
            solution.task_type == task_type
            and solution.task_id == task_id
            and solution.user_id == user_id
        )
        return sorted(solutions, key=lambda solution: solution.score)[-1]

    async def create_solution(self, solution: AnySolution) -> None:
        self.solutions[solution.uid] = solution

    async def store_solution_check_result(
        self,
        solution_id: str,
        score: int,
        detailed_verdict: str,
        short_verdict: str,
        group_scores: dict[str, int],
        protocol: dict[str, Any]
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
        task_id: int
    ) -> None:
        for solution_id, solution in self.solutions.items():
            if solution.task_id == task_id and solution.task_type == task_type:
                self.solutions.pop(solution_id)


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
    async def get_contest_managers(self, contest_id: int) -> Sequence[int]:
        pass

    async def get_contest_tasks(self, contest_id: int) -> Sequence[
        ContestTaskHead]:
        pass

    async def get_contest_participants(self, contest_id: int) -> Sequence[int]:
        pass

    async def can_submit(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int
    ) -> bool:
        pass

    async def get_task(
        self,
        task_type: str,
        task_id: int
    ) -> AnyTaskDTO | None:
        pass

    async def get_quiz_task(self, task_id: int) -> QuizTaskDTO | None:
        pass

    async def get_code_task(self, task_id: int) -> CodeTaskDTO | None:
        pass
