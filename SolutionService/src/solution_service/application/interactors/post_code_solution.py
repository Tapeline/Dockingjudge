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
from solution_service.application.interfaces.account import User
from solution_service.application.interfaces.contest import (
    CodeTaskDTO,
    ContestService,
)
from solution_service.application.interfaces.publisher import SolutionPublisher
from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.storage import (
    DBSession,
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
    """Posts a code solution."""

    object_storage: Storage
    solutions: SolutionRepository
    contest_service: ContestService
    solution_publisher: SolutionPublisher
    config: Config
    user_idp: UserIdProvider
    id_gen: IdGenerator
    session: DBSession

    async def __call__(
        self,
        solution: NewCodeSolution,
    ) -> CodeSolution:
        """Posts a code solution."""
        user = await self.user_idp.require_user()
        logger.info("Getting code task %s", solution.task_id)
        task = await self._retrieve_task(solution)
        await self._ensure_can_submit(task, user)
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
        await self.session.commit()
        return solution_entity

    async def _ensure_can_submit(self, task: CodeTaskDTO, user: User) -> None:
        can_submit = await self.contest_service.can_submit(
            user.id, TaskType.CODE, task.id,
        )
        if not can_submit:
            logger.info("Rejecting submit request")
            raise MayNotSubmitSolution

    async def _retrieve_task(self, solution: NewCodeSolution) -> CodeTaskDTO:
        task = await self.contest_service.get_code_task(solution.task_id)
        if not task:
            logger.warning("No task %s", solution.task_id)
            raise NotFound
        return task

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
                    name=_DEFAULT_FILENAME.format(f"{uuid.uuid4()}.zip"),
                    contents=base64.b64decode(solution.text),
                    encoding=self.config.encoding,
                )
            case _:
                assert_never(
                    solution.submission_type,  # type: ignore[arg-type]
                )
