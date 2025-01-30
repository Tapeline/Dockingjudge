from typing import Annotated
from uuid import UUID

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, HttpMethod, route, Request, get
from litestar.datastructures import State
from litestar.params import Body

from solution_service.application import interactors, dto
from solution_service.application.interfaces.account import UserDTO
from solution_service.application.interfaces.contest import AbstractContestService
from solution_service.controllers import schemas
from solution_service.application.exceptions import NotFoundException, ForbiddenException
from solution_service.domain.entities.abstract import TaskType, AnySolution
from solution_service.infrastructure.account_service import authenticated_user_guard


def _serialize_solution(
        solution: AnySolution,
        is_safe: bool = False,
) -> schemas.SolutionSchema:
    data = None
    if not is_safe and solution.task_type == TaskType.QUIZ:
        data = schemas.QuizSolutionExtraSchema(
            submitted_answer=solution.submitted_answer,
        )
    if not is_safe and solution.task_type == TaskType.CODE:
        data = schemas.CodeSolutionExtraSchema(
            compiler=solution.compiler_name,
            submission_url=solution.submission_url,
            group_scores=solution.group_scores,
            detailed_verdict=solution.detailed_verdict,
        )
    return schemas.SolutionSchema(
        id=solution.uid,
        task_id=solution.task_id,
        task_type=solution.task_type,
        user_id=solution.user_id,
        score=solution.score,
        short_verdict=solution.short_verdict,
        submitted_at=solution.submitted_at,
        data=data,
    )


inject_guards = {"guards": [authenticated_user_guard]}


class SolutionsController(Controller):
    path = "/api/v1/solutions"
    security = [{"jwt_auth": []}]

    @route(
        http_method=HttpMethod.GET,
        path="/{solution_uid:uuid}/",
        **inject_guards
    )
    @inject
    async def get_solution(
            self,
            solution_uid: Annotated[UUID, Body(description="Solution ID")],
            interactor: Depends[interactors.GetSolution],
            contest_service: Depends[AbstractContestService],
            request: Request[UserDTO, ..., State],
    ) -> schemas.SolutionSchema:
        solution = await interactor(solution_id=str(solution_uid))
        print(solution_uid)
        if solution is None:
            raise NotFoundException
        contest_managers = await contest_service.get_contest_managers(solution.contest_id)
        if request.user.id != solution.user_id and request.user.id not in contest_managers:
            raise ForbiddenException
        return _serialize_solution(solution)

    @route(
        http_method=HttpMethod.GET,
        path="/my/",
        **inject_guards
    )
    @inject
    async def get_my_solutions(
            self,
            request: Request[UserDTO, ..., State],
            interactor: Depends[interactors.ListSolutionForUser],
    ) -> list[schemas.SolutionSchema]:
        solutions = await interactor(request.user.id)
        return list(map(_serialize_solution, solutions))

    @route(
        http_method=HttpMethod.GET,
        path="/my/{task_type:str}/{task_id:int}/",
        **inject_guards
    )
    @inject
    async def get_my_solutions_for_task(
            self,
            request: Request[UserDTO, ..., State],
            interactor: Depends[interactors.ListSolutionForUserOnTask],
            task_type: str,
            task_id: int,
    ) -> list[schemas.SolutionSchema]:
        print("REQ")
        solutions = await interactor(request.user.id, TaskType(task_type), task_id)
        return list(map(_serialize_solution, solutions))

    @route(
        http_method=HttpMethod.POST,
        path="/post/code/{task_id:int}/",
        **inject_guards
    )
    @inject
    async def post_code_solution(
            self,
            request: Request[UserDTO, ..., State],
            data: schemas.PostCodeSolutionSchema,
            task_id: int,
            interactor: Depends[interactors.PostCodeSolution],
    ) -> schemas.SolutionSchema:
        solution = await interactor(
            request.user.id,
            dto.NewCodeSolution(
                compiler=data.compiler,
                text=data.text,
                submission_type=data.submission_type,
                task_id=task_id,
                main_file=data.main_file,
            ),
        )
        return _serialize_solution(solution)

    @route(
        http_method=HttpMethod.POST,
        path="/post/quiz/{task_id:int}/",
        **inject_guards
    )
    @inject
    async def post_quiz_solution(
            self,
            request: Request[UserDTO, ..., State],
            data: schemas.PostQuizSolutionSchema,
            task_id: int,
            interactor: Depends[interactors.PostQuizSolution],
    ) -> schemas.SolutionSchema:
        solution = await interactor(
            request.user.id,
            dto.NewQuizSolution(
                text=data.text,
                task_id=task_id,
            ),
        )
        return _serialize_solution(solution)

    @route(
        http_method=HttpMethod.GET,
        path="/score/",
        **inject_guards
    )
    @inject
    async def get_score_for_tasks(
            self,
            request: Request[UserDTO, ..., State],
            tasks: list[str],
            interactor: Depends[interactors.GetBestSolutionForUserOnTask],
    ) -> list[schemas.SolutionSchema]:
        tasks = map(lambda x: x.split(":"), tasks)
        tasks = [(str(x[0]), int(x[1])) for x in tasks]
        return [
            _serialize_solution(await interactor(request.user.id, *task), is_safe=True)
            for task in tasks
        ]

    @route(
        http_method=HttpMethod.GET,
        path="/standings/{contest_id:int}/",
        **inject_guards
    )
    @inject
    async def get_standings(
            self,
            contest_id: int,
            interactor: Depends[interactors.GetStandings],
    ) -> schemas.StandingsSchema:
        standings, tasks = await interactor(contest_id)
        return schemas.StandingsSchema(
            tasks=tasks,
            table=[
                schemas.UserContestStatusSchema(
                    user=schemas.UserSchema(
                        id=status.user.id,
                        username=status.user.username,
                        profile_pic=status.user.profile_pic,
                        roles=status.user.roles,
                    ),
                    tasks_attempted=status.tasks_attempted,
                    tasks_solved=status.tasks_solved,
                    solutions=[
                        _serialize_solution(solution, is_safe=True)
                        for solution in status.solutions
                    ],
                    total_score=status.total_score,
                )
                for status in standings
            ]
        )


@get("/api/v1/solutions/ping/", exclude_from_auth=True)
@inject
async def ping() -> str:
    return "ok"
