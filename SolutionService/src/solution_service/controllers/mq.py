import asyncio
import logging
from typing import Any, Final, override

from dishka import FromDishka
from faststream.rabbit import (
    RabbitBroker,
    RabbitExchange,
    RabbitQueue,
    RabbitRouter,
)

from solution_service.application.dto import SolutionCheckResult
from solution_service.application.interactors.purge_solutions import (
    PurgeTaskSolutions,
    PurgeUserSolutions,
)
from solution_service.application.interactors.update_solution import (
    StoreCheckedSolution,
)
from solution_service.application.interfaces.publisher import SolutionPublisher
from solution_service.application.interfaces.storage import Storage
from solution_service.controllers.event_schemas import (
    MQContestEvent,
    MQSolutionAnswer,
    MQTaskEvent,
    MQUserEvent,
)
from solution_service.domain.abstract import CodeSolution, TaskType

_DELETION_EVENT: Final = "DELETED"

logger = logging.getLogger(__name__)
mq_controller = RabbitRouter()

solutions_exchange = RabbitExchange("solutions_exchange", durable=True)
answers_exchange = RabbitExchange("judge_answers_exchange", durable=True)
user_object_events = RabbitExchange("user_object_events", durable=True)
contest_object_events = RabbitExchange("contest_object_events", durable=True)

answers_inbox = RabbitQueue(
    "_solution_service_inbox",
    durable=True,
    routing_key="solution_answer",
)
user_event_inbox = RabbitQueue(
    "_solution_service_user_inbox",
    durable=True,
    routing_key="user_event",
)
contest_event_inbox = RabbitQueue(
    "_solution_service_contest_inbox",
    durable=True,
    routing_key="contest_event",
)
quiz_task_event_inbox = RabbitQueue(
    "_solution_service_quiz_task_inbox",
    durable=True,
    routing_key="quiz_task_event",
)
code_task_event_inbox = RabbitQueue(
    "_solution_service_code_task_inbox",
    durable=True,
    routing_key="code_task_event",
)


@mq_controller.subscriber(answers_inbox, answers_exchange)
async def handle_checked_solution(
    data: MQSolutionAnswer,
    interactor: FromDishka[StoreCheckedSolution],
) -> None:
    logger.info("Received solution answer for %s", data.id)
    await interactor(
        data.id,
        SolutionCheckResult(
            detailed_verdict=data.detailed_verdict,
            short_verdict=data.short_verdict,
            score=data.score,
            group_scores=data.group_scores,
            protocol=data.protocol,
        ),
    )
    logger.info("Updated solution %s in db", data.id)


class RMQSolutionPublisher(SolutionPublisher):
    def __init__(
        self,
        storage: FromDishka[Storage],
        broker: FromDishka[RabbitBroker],
    ) -> None:
        self.storage = storage
        self.broker = broker
        self.logger = logging.getLogger("solution publisher")

    @override
    async def publish(
        self, solution: CodeSolution, test_suite: dict[str, Any],
    ) -> None:
        await self.broker.publish(
            {
                "id": f"{solution.uid}",
                "solution_url": solution.submission_url,
                "main_file": solution.main_file,
                "submission_type": solution.submission_type.value,
                "compiler": solution.compiler_name,
                "suite": test_suite,
            },
            exchange=solutions_exchange,
            routing_key="solution_to_check",
        )
        self.logger.info("Published solution #%s", solution.uid)


@mq_controller.subscriber(user_event_inbox, user_object_events)
async def handle_user_deleted(
    data: MQUserEvent,
    interactor: FromDishka[PurgeUserSolutions],
) -> None:
    if data.event != _DELETION_EVENT:
        return
    logger.info("Received purge request for user %s", data.object.id)
    await interactor(data.object.id)
    logger.info("Purged user %s", data.object.id)


@mq_controller.subscriber(contest_event_inbox, contest_object_events)
async def handle_contest_deleted(
    data: MQContestEvent,
    interactor: FromDishka[PurgeTaskSolutions],
) -> None:
    if data.event != _DELETION_EVENT:
        return
    logger.info("Received purge request for contest %s", data.object.id)
    # TODO: that's inefficient
    await asyncio.gather(
        *(
            interactor(page.type, page.id)
            for page in data.object.pages
        ),
    )
    logger.info("Purged contest %s", data.object.id)


@mq_controller.subscriber(quiz_task_event_inbox, contest_object_events)
async def handle_quiz_task_deleted(
    data: MQTaskEvent,
    interactor: FromDishka[PurgeTaskSolutions],
) -> None:
    if data.event != _DELETION_EVENT:
        return
    logger.info("Received purge request for task quiz:%s", data.object.id)
    await interactor(TaskType.QUIZ, data.object.id)
    logger.info("Purged task quiz:%s", data.object.id)


@mq_controller.subscriber(code_task_event_inbox, contest_object_events)
async def handle_code_task_deleted(
    data: MQTaskEvent,
    interactor: FromDishka[PurgeTaskSolutions],
) -> None:
    if data.event != _DELETION_EVENT:
        return
    logger.info("Received purge request for task code:%s", data.object.id)
    await interactor(TaskType.CODE, data.object.id)
    logger.info("Purged task code:%s", data.object.id)
