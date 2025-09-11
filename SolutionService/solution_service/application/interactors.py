import base64
import logging
import uuid
from collections.abc import Collection, Sequence
from operator import itemgetter

from solution_service.application import dto
from solution_service.application.checker_loader import load_checker
from solution_service.application.dto import SolutionCheckResult
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
            list(map(itemgetter(slice(0, 2)), tasks)),
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
        self.logger = logging.getLogger("get_standings")

    async def __call__(
        self,
        contest_id: int
    ) -> tuple[
        Sequence[dto.EnrichedUserContestStatus],
        Sequence[tuple[TaskType, int, str]]
    ]:
        self.logger.info("Getting participants")
        participants = await self._contest_service.get_contest_participants(contest_id)
        self.logger.info("Getting user objects")
        participant_objects = await self._account_service.get_users_by_ids(participants)
        self.logger.info("Getting contest tasks")
        contest_tasks = await self._contest_service.get_contest_tasks(contest_id)
        contest_tasks_ids = list(map(itemgetter(slice(0, 2)), contest_tasks))
        self.logger.info("Requesting standings")
        standings = await self._solution_repo.get_contest_standings(
            contest_tasks_ids,
            participants
        )
        self.logger.info("Serializing standings")
        self.logger.info("%s", str(standings))
        return [
            dto.EnrichedUserContestStatus(
                user=participant_objects[i],
                solutions=standings[i].solutions,
                tasks_solved=standings[i].tasks_solved,
                tasks_attempted=standings[i].tasks_attempted,
                total_score=standings[i].total_score,
            )
            for i, row in enumerate(standings)
        ], contest_tasks


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
        self.logger = logging.getLogger("post_code")

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
        self.logger.info("Getting code task %s", solution.task_id)
        task = await self._contest_service.get_code_task(solution.task_id)
        if task is None:
            raise NotFoundException
        self.logger.info("Saving file")
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
            compiler_name=solution.compiler,
            main_file=solution.main_file,
            submission_type=solution.submission_type,
        )
        self.logger.info("Creating solution")
        solution_id = await self._solution_repo.create_solution(solution_entity)
        solution_entity.uid = solution_id
        self.logger.info("Publishing solution")
        await self._publisher.publish(solution_entity, task.test_suite)
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
        self.logger = logging.getLogger("post_code")

    async def __call__(
        self,
        user_id: int,
        solution: dto.NewQuizSolution
    ) -> QuizSolution:
        self.logger.info("Getting quiz task %s", solution.task_id)
        task = await self._contest_service.get_quiz_task(solution.task_id)
        self.logger.info(
            "Loading checker %s %s", task.validator.type, task.validator.args
        )
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
        self.logger.info("Checking quiz solution for task %s", task.id)
        use_case(solution_entity)
        self.logger.info("Saving solution")
        solution_id = await self._solution_repo.create_solution(solution_entity)
        solution_entity.uid = solution_id
        return solution_entity


class StoreCheckedSolution:
    def __init__(
            self,
            solution_repository: solutions.AbstractSolutionRepository,
    ) -> None:
        self.solution_repo = solution_repository

    async def __call__(
            self,
            solution_id: str,
            check_result: SolutionCheckResult
    ) -> None:
        await self.solution_repo.store_solution_check_result(
            solution_id,
            check_result.score,
            check_result.detailed_verdict,
            check_result.short_verdict,
            check_result.group_scores,
            check_result.protocol,
        )


class PurgeUserSolutions:
    def __init__(
            self,
            solution_repository: solutions.AbstractSolutionRepository,
    ) -> None:
        self.solution_repo = solution_repository

    async def __call__(self, user_id: int) -> None:
        await self.solution_repo.purge_user_solutions(user_id)
        

class PurgeTaskSolutions:
    def __init__(
            self,
            solution_repository: solutions.AbstractSolutionRepository,
    ) -> None:
        self.solution_repo = solution_repository

    async def __call__(self, task_type: TaskType, task_id: int) -> None:
        await self.solution_repo.purge_task_solutions(task_type, task_id)
