import logging
from collections.abc import Sequence
from dataclasses import dataclass
from operator import itemgetter

from solution_service.application.dto import (
    EnrichedUserContestStatus,
    EnrichedUserStandingRow,
)
from solution_service.application.interfaces.account import AccountService
from solution_service.application.interfaces.contest import (
    ContestService,
    ContestTaskHead,
)
from solution_service.application.interfaces.solutions import \
    SolutionRepository

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class GetStandings:
    solution_repository: SolutionRepository
    contest_service: ContestService
    account_service: AccountService

    async def __call__(
        self,
        contest_id: int
    ) -> tuple[
        Sequence[EnrichedUserStandingRow],
        Sequence[ContestTaskHead]
    ]:
        logger.info("Getting participants")
        participants = await self.contest_service.get_contest_participants(contest_id)
        logger.info("Getting user objects")
        participant_objects = await self.account_service.get_users_by_ids(participants)
        logger.info("Getting contest tasks")
        contest_tasks = await self.contest_service.get_contest_tasks(contest_id)
        contest_tasks_ids = list(map(itemgetter(slice(0, 2)), contest_tasks))
        logger.info("Requesting standings")
        standings = await self.solution_repository.get_contest_standings(
            contest_tasks_ids,
            participants
        )
        logger.info("Serializing standings %s", str(standings))
        return [
            EnrichedUserStandingRow(
                user=participant_objects[i],
                solutions=standings[i].solutions,
                tasks_solved=standings[i].tasks_solved,
                tasks_attempted=standings[i].tasks_attempted,
                total_score=standings[i].total_score,
            )
            for i, row in enumerate(standings)
        ], contest_tasks
