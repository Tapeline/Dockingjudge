import base64
import logging
import uuid
from dataclasses import dataclass
from typing import Final, assert_never

from solution_service.application.dto import NewCodeSolution
from solution_service.application.exceptions import (
    MayNotSubmitSolution,
    NotFound,
)
from solution_service.application.interfaces.contest import ContestService
from solution_service.application.interfaces.publisher import SolutionPublisher
from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.storage import (
    File,
    IdGenerator,
    Storage,
)
from solution_service.application.interfaces.user import UserIdProvider
from solution_service.config import Config
from solution_service.domain.abstract import CodeSolution, TaskType

logger = logging.getLogger(__name__)

_DEFAULT_FILENAME: Final = "file{0}"


@dataclass(frozen=True, slots=True)
class PostCodeSolution:
    object_storage: Storage
    solutions: SolutionRepository
    contest_service: ContestService
    solution_publisher: SolutionPublisher
    config: Config
    user_idp: UserIdProvider
    id_gen: IdGenerator

    async def __call__(
        self,
        solution: NewCodeSolution,
    ) -> CodeSolution:
        user = await self.user_idp.require_user()
        logger.info("Getting code task %s", solution.task_id)
        task = await self.contest_service.get_code_task(solution.task_id)
        if task is None:
            raise NotFound
        can_submit = await self.contest_service.can_submit(
            user.id, TaskType.CODE, task.id,
        )
        if not can_submit:
            logger.info("Rejecting submit request")
            raise MayNotSubmitSolution
        logger.info("Saving file")
        solution_file = self._prepare_file(solution)
        solution_url = await self.object_storage.save_file(solution_file)
        solution_entity = CodeSolution(
            uid=self.id_gen.new_id(),
            contest_id=task.contest_id,
            task_id=solution.task_id,
            task_type=TaskType.CODE,
            user_id=user.id,
            score=0,
            short_verdict="NC",
            submission_url=solution_url,
            compiler_name=solution.compiler,
            main_file=solution.main_file,
            submission_type=solution.submission_type,
        )
        logger.info("Creating solution")
        await self.solutions.create_solution(solution_entity)
        logger.info("Publishing solution")
        await self.solution_publisher.publish(solution_entity, task.test_suite)
        return solution_entity

    def _prepare_file(self, solution: NewCodeSolution) -> File:
        match solution.submission_type.value:
            case "str":
                return File(
                    name=_DEFAULT_FILENAME.format(str(uuid.uuid4())),
                    contents=solution.text.encode(self.config.encoding),
                    encoding=self.config.encoding,
                )
            case "zip":
                return File(
                    name=_DEFAULT_FILENAME.format(str(uuid.uuid4()) + ".zip"),
                    contents=base64.b64decode(solution.text),
                    encoding=self.config.encoding,
                )
            case _:
                assert_never(solution.submission_type)
