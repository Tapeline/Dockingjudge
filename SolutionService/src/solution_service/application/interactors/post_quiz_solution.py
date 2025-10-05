import logging
from dataclasses import dataclass

from solution_service.application.checker_loader import load_checker
from solution_service.application.dto import NewQuizSolution
from solution_service.application.exceptions import (
    MayNotSubmitSolution,
    NotFound,
)
from solution_service.application.interfaces.contest import ContestService
from solution_service.application.interfaces.solutions import (
    SolutionRepository,
)
from solution_service.application.interfaces.storage import (
    DBSession,
    IdGenerator,
)
from solution_service.application.interfaces.user import UserIdProvider
from solution_service.config import Config
from solution_service.domain.abstract import QuizSolution, TaskType

logger = logging.getLogger(__name__)


class CheckerNotFoundException(NotFound):
    """Raised when a checker is not found."""

    def __init__(self, checker_name: str) -> None:
        super().__init__(checker_name)
        self.checker_name = checker_name
        self.add_note(f"Checker name: {checker_name}")


@dataclass(frozen=True, slots=True)
class PostQuizSolution:
    """Posts a quiz solution."""

    solution_repository: SolutionRepository
    contest_service: ContestService
    config: Config
    user_idp: UserIdProvider
    id_gen: IdGenerator
    session: DBSession

    async def __call__(
        self,
        solution: NewQuizSolution,
    ) -> QuizSolution:
        user = await self.user_idp.require_user()
        logger.info("Getting quiz task %s", solution.task_id)
        task = await self.contest_service.get_quiz_task(solution.task_id)
        if not task:
            logger.warning("No task %s", solution.task_id)
            raise NotFound
        can_submit = await self.contest_service.can_submit(
            user.id, TaskType.QUIZ, task.id,
        )
        if not can_submit:
            logger.info("Rejecting submit request")
            raise MayNotSubmitSolution
        logger.info(
            "Loading checker %s %s", task.validator.type, task.validator.args,
        )
        checker = load_checker(
            task.validator.type,
            task.validator.args,
            task.points,
        )
        if checker is None:
            raise CheckerNotFoundException(task.validator.type)
        solution_entity = QuizSolution(
            uid=self.id_gen.new_id(),
            contest_id=task.contest_id,
            task_id=solution.task_id,
            task_type=TaskType.QUIZ,
            user_id=user.id,
            score=0,
            short_verdict="NC",
            submitted_answer=solution.text,
        )
        logger.info("Checking quiz solution for task %s", task.id)
        verdict = checker.check(solution_entity.submitted_answer)
        solution_entity.short_verdict = (
            "OK" if verdict.is_successful else "WA"
        )
        solution_entity.score = verdict.score
        logger.info("Saving solution")
        await self.solution_repository.create_solution(solution_entity)
        await self.session.commit()
        return solution_entity
