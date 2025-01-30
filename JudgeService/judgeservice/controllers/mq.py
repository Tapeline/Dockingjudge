from logging import Logger

from dishka import FromDishka
from faststream.rabbit import RabbitRouter, RabbitExchange, RabbitQueue

from judgeservice.application.interactors import ProcessSolutionInteractor
from judgeservice.controllers.schemas import MQSolutionCheckRequest, MQSolutionAnswer
from judgeservice.domain.entities import Solution

mq_controller = RabbitRouter()

solutions_exchange = RabbitExchange("solutions_exchange", durable=True)
answers_exchange = RabbitExchange("judge_answers_exchange", durable=True)

service_inbox = RabbitQueue("_judge_service_inbox", durable=True, routing_key="solution_to_check")


@mq_controller.subscriber(service_inbox, solutions_exchange)
@mq_controller.publisher(exchange=answers_exchange, routing_key="solution_answer")
async def handle_incoming_solution(
        data: MQSolutionCheckRequest,
        interactor: FromDishka[ProcessSolutionInteractor],
) -> MQSolutionAnswer:
    print("Received request %s" % data.id)
    solution = Solution(
        id=data.id,
        solution_url=data.solution_url,
        solution_data=None,
        main_file=data.main_file,
        submission_type=data.submission_type,
        compiler=data.compiler,
        suite=data.suite,
        score=0,
        short_verdict="",
        group_scores={},
        detailed_verdict="",
        protocol={}
    )
    await interactor(solution)
    print("Handled request %s" % data.id)
    return MQSolutionAnswer(
        id=data.id,
        score=solution.score,
        short_verdict=solution.short_verdict,
        group_scores=solution.group_scores,
        detailed_verdict=solution.detailed_verdict,
        protocol=solution.protocol,
    )
