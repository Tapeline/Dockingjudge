import base64
import uuid
from collections.abc import Collection, Sequence

from solution_service.application import dto
from solution_service.application.checker_loader import load_checker
from solution_service.application.exceptions import NotFoundException
from solution_service.application.interfaces import (
    account,
    contest,
    publisher,
    solutions,
    storage,
)
from solution_service.config import Config
from solution_service.domain.entities.abstract import AnySolution, CodeSolution, TaskType, QuizSolution
from solution_service.domain.usecases.check import CheckQuizSolution


class ListSolutionForUser:
    all_solutions = None  # alias

    def __init__(
        self,
        solution_repository: solutions.AbstractSolutionRepository,
    ):
        self._solution_repo = solution_repository

    async def __call__(
        self,
        user_id: int,
    ) -> Collection[AnySolution]:
        return await self._solution_repo.get_all_solutions_of_user(
            user_id,
            self.all_solutions,
        )


class ListSolutionForUserOnContest:
    def __init__(
        self,
        solution_repository: solutions.AbstractSolutionRepository,
        contest_service: contest.AbstractContestService,
    ):
        self._solution_repo = solution_repository
        self._contest_service = contest_service

    async def __call__(
        self,
        user_id: int,
        contest_id: int,
    ) -> Sequence[solutions.AnySolution]:
        tasks = await self._contest_service.get_contest_tasks(contest_id)
        return await self._solution_repo.get_all_solutions_of_user_for_contest(
            user_id,
            tasks,
        )


class ListSolutionForUserOnTask:
    def __init__(
        self,
        solution_repository: solutions.AbstractSolutionRepository,
        contest_service: contest.AbstractContestService,
    ):
        self._solution_repo = solution_repository
        self._contest_service = contest_service

    async def __call__(
        self,
        user_id: int,
        task_type: TaskType,
        task_id: int,
    ) -> Sequence[solutions.AnySolution]:
        print("REQUEST")
        return await self._solution_repo.get_all_solutions_of_task(
            user_id,
            task_type,
            task_id
        )


class GetStandings:
    def __init__(
        self,
        solution_repository: solutions.AbstractSolutionRepository,
        contest_service: contest.AbstractContestService,
        account_service: account.AbstractAccountService,
    ):
        self._solution_repo = solution_repository
        self._contest_service = contest_service
        self._account_service = account_service

    async def __call__(
        self,
        contest_id: int
    ) -> Sequence[dto.EnrichedUserContestStatus]:
        participants = await self._contest_service.get_contest_participants(contest_id)
        participant_objects = await self._account_service.get_users_by_ids(participants)
        contest_tasks = await self._contest_service.get_contest_tasks(contest_id)
        standings = await self._solution_repo.get_contest_standings(
            contest_tasks,
            participants
        )
        return [
            dto.EnrichedUserContestStatus(
                user=participant_objects[i],
                solutions=standings[i].solutions,
                tasks_solved=standings[i].tasks_solved,
                tasks_attempted=standings[i].tasks_attempted,
                total_score=standings[i].total_score,
            )
            for i, row in enumerate(standings)
        ]


class GetBestSolutionForUserOnTask:
    def __init__(
        self,
        solution_repository: solutions.AbstractSolutionRepository,
    ):
        self._solution_repo = solution_repository

    async def __call__(
        self,
        user_id: int,
        task_type: str,
        task_id: int
    ) -> AnySolution:
        return await self._solution_repo.get_best_solution_by_user_task(
            user_id,
            TaskType(task_type),
            task_id,
        )


class GetSolution:
    def __init__(
        self,
        solution_repository: solutions.AbstractSolutionRepository,
    ):
        self._solution_repo = solution_repository

    async def __call__(self, solution_id: str) -> AnySolution:
        print("Getting", solution_id)
        return await self._solution_repo.get_solution(solution_id)


class PostCodeSolution:
    default_filename = "file{0}"

    def __init__(
        self,
        object_storage: storage.AbstractStorage,
        solution_repository: solutions.AbstractSolutionRepository,
        contest_service: contest.AbstractContestService,
        solution_publisher: publisher.AbstractSolutionPublisher,
        config: Config
    ):
        self._solution_repo = solution_repository
        self._contest_service = contest_service
        self._encoding = config.encoding
        self._storage = object_storage
        self._publisher = solution_publisher

    def _prepare_file(self, solution: dto.NewCodeSolution) -> storage.File:
        match solution.submission_type.value:
            case "str":
                return self._prepare_file_str(solution.text)
            case "zip":
                return self._prepare_file_zip(solution.text)
            case _:
                raise ValueError(
                    f"Solution is of undefined type "
                    f"{solution.submission_type}"
                )

    def _prepare_file_str(self, text: str) -> storage.File:
        return storage.File(
            name=self.default_filename.format(str(uuid.uuid4())),
            contents=text.encode(self._encoding),
            encoding=self._encoding,
        )

    def _prepare_file_zip(self, text: str) -> storage.File:
        return storage.File(
            name=self.default_filename.format(str(uuid.uuid4()) + ".zip"),
            contents=base64.b64decode(text),
            encoding=self._encoding,
        )

    async def __call__(
            self,
            user_id: int,
            solution: dto.NewCodeSolution
    ) -> CodeSolution:
        task = await self._contest_service.get_code_task(solution.task_id)
        if task is None:
            raise NotFoundException
        solution_file = self._prepare_file(solution)
        solution_url = await self._storage.save_file(solution_file)
        solution_entity = CodeSolution(
            uid=...,
            contest_id=task.contest_id,
            task_id=solution.task_id,
            task_type=TaskType.CODE,
            user_id=user_id,
            score=0,
            short_verdict="NC",
            submission_url=solution_url,
        )
        solution_id = await self._solution_repo.create_solution(solution_entity)
        solution_entity.uid = solution_id
        self._publisher.publish(solution_entity)
        return solution_entity


class CheckerNotFoundException(NotFoundException):
    def __init__(self, checker_name: str):
        super().__init__(checker_name=checker_name)
        self.checker_name = checker_name
        self.add_note(f"Checker name: {checker_name}")


class PostQuizSolution:
    def __init__(
            self,
            solution_repository: solutions.AbstractSolutionRepository,
            contest_service: contest.AbstractContestService,
            account_service: account.AbstractAccountService,
            solution_publisher: publisher.AbstractSolutionPublisher,
            config: Config,
    ):
        self._solution_repo = solution_repository
        self._contest_service = contest_service
        self._account_service = account_service
        self._encoding = config.encoding
        self._publisher = solution_publisher

    async def __call__(
        self,
        user_id: int,
        solution: dto.NewQuizSolution
    ) -> QuizSolution:
        task = await self._contest_service.get_quiz_task(solution.task_id)
        checker = load_checker(
            task.validator.type,
            task.validator.args,
            task.points
        )
        if checker is None:
            raise CheckerNotFoundException(task.validator.type)
        use_case = CheckQuizSolution(checker)
        solution_entity = QuizSolution(
            uid=...,
            contest_id=task.contest_id,
            task_id=solution.task_id,
            task_type=TaskType.QUIZ,
            user_id=user_id,
            score=0,
            short_verdict="NC",
            submitted_answer=solution.text
        )
        use_case(solution_entity)
        solution_id = await self._solution_repo.create_solution(solution_entity)
        solution_entity.uid = solution_id
        return solution_entity
