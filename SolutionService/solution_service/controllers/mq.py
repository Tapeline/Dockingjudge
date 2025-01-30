import logging
from logging import Logger

from dishka import FromDishka
from faststream.rabbit import RabbitRouter, RabbitExchange, RabbitQueue, RabbitBroker

from solution_service.application.dto import SolutionCheckResult
from solution_service.application.interactors import StoreCheckedSolution
from solution_service.application.interfaces.publisher import AbstractSolutionPublisher
from solution_service.application.interfaces.storage import AbstractStorage
from solution_service.controllers.schemas import MQSolutionAnswer
from solution_service.domain.entities.abstract import CodeSolution

mq_controller = RabbitRouter()

solutions_exchange = RabbitExchange("solutions_exchange", durable=True)
answers_exchange = RabbitExchange("judge_answers_exchange", durable=True)

answers_inbox = RabbitQueue("_solution_service_inbox", durable=True)


@mq_controller.subscriber(answers_inbox, solutions_exchange)
async def handle_checked_solution(
        data: MQSolutionAnswer,
        interactor: FromDishka[StoreCheckedSolution]
):
    logging.info("Received solution answer for %s", data.id)
    await interactor(
        data.id,
        SolutionCheckResult(
            detailed_verdict=data.detailed_verdict,
            short_verdict=data.short_verdict,
            score=data.score,
            group_scores=data.group_scores,
            protocol=data.protocol,
        )
    )
    logging.info("Updated solution %s in db", data.id)


class RMQSolutionPublisher(AbstractSolutionPublisher):
    def __init__(
            self,
            storage: FromDishka[AbstractStorage],
            broker: FromDishka[RabbitBroker]
    ):
        self.storage = storage
        self.broker = broker
        self.logger = logging.getLogger("solution publisher")

    async def publish(self, solution: CodeSolution, test_suite: dict) -> None:
        await self.broker.publish(
            {
                "id": f"{solution.uid}",
                "solution_url": solution.submission_url,
                "main_file": solution.main_file,
                "submission_type": solution.submission_type.value,
                "compiler": solution.compiler_name,
                "suite": test_suite
            },
            exchange=solutions_exchange,
            routing_key="solution_to_check"
        )
        self.logger.info(f"Published solution #{solution.uid}")
