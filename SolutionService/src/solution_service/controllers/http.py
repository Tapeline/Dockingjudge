import asyncio
from typing import Annotated
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, HttpMethod, get, route
from litestar.params import Body

from solution_service.application import dto
from solution_service.application.exceptions import NotFound
from solution_service.application.interactors.get_solution import (
    GetBestSolutionForUserOnTask,
    GetSolution,
)
from solution_service.application.interactors.list_solutions import (
    ListMySolutions,
    ListMySolutionsOnTask,
)
from solution_service.application.interactors.post_code_solution import (
    PostCodeSolution,
)
from solution_service.application.interactors.post_quiz_solution import (
    PostQuizSolution,
)
from solution_service.application.interactors.standings import GetStandings
from solution_service.controllers import schemas
from solution_service.controllers.dumping import serialize_solution
from solution_service.controllers.loading import load_composite_task_id
from solution_service.domain.abstract import TaskType
from solution_service.infrastructure.account_service import (
    authenticated_user_guard,
)

inject_guards = {"guards": [authenticated_user_guard]}


class SolutionsController(Controller):
    path = "/api/v1/solutions"
    security = ({"jwt_auth": []},)  # type: ignore[mutable-override]

    @route(
        http_method=HttpMethod.GET,
        path="/{solution_uid:uuid}/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def get_solution(
        self,
        solution_uid: Annotated[UUID, Body(description="Solution ID")],
        interactor: Depends[GetSolution],
    ) -> schemas.SolutionSchema:
        solution = await interactor(solution_id=str(solution_uid))
        if solution is None:
            raise NotFound
        return serialize_solution(solution)

    @route(
        http_method=HttpMethod.GET,
        path="/my/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def get_my_solutions(
        self,
        interactor: Depends[ListMySolutions],
    ) -> list[schemas.SolutionSchema]:
        solutions = await interactor()
        return list(map(serialize_solution, solutions))

    @route(
        http_method=HttpMethod.GET,
        path="/my/{task_type:str}/{task_id:int}/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def get_my_solutions_for_task(
        self,
        interactor: Depends[ListMySolutionsOnTask],
        task_type: str,
        task_id: int,
    ) -> list[schemas.SolutionSchema]:
        solutions = await interactor(TaskType(task_type), task_id)
        return list(map(serialize_solution, solutions))

    @route(
        http_method=HttpMethod.POST,
        path="/post/code/{task_id:int}/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def post_code_solution(
        self,
        data: schemas.PostCodeSolutionSchema,
        task_id: int,
        interactor: Depends[PostCodeSolution],
    ) -> schemas.SolutionSchema:
        solution = await interactor(
            dto.NewCodeSolution(
                compiler=data.compiler,
                text=data.text,
                submission_type=data.submission_type,
                task_id=task_id,
                main_file=data.main_file,
            ),
        )
        return serialize_solution(solution)

    @route(
        http_method=HttpMethod.POST,
        path="/post/quiz/{task_id:int}/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def post_quiz_solution(
        self,
        data: schemas.PostQuizSolutionSchema,
        task_id: int,
        interactor: Depends[PostQuizSolution],
    ) -> schemas.SolutionSchema:
        solution = await interactor(
            dto.NewQuizSolution(
                text=data.text,
                task_id=task_id,
            ),
        )
        return serialize_solution(solution)

    @route(
        http_method=HttpMethod.GET,
        path="/score/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def get_score_for_tasks(
        self,
        tasks: list[str],
        interactor: Depends[GetBestSolutionForUserOnTask],
    ) -> list[schemas.SolutionSchema | None]:
        tasks_ids = map(load_composite_task_id, tasks)
        solution_dms = await asyncio.gather(*(
            interactor(task_type, task_id)
            for task_type, task_id in tasks_ids
        ))
        return [
            serialize_solution(solution, is_safe=True)
            for solution in solution_dms
        ]

    @route(
        http_method=HttpMethod.GET,
        path="/standings/{contest_id:int}/",
        **inject_guards,  # type: ignore[arg-type]
    )
    @inject
    async def get_standings(
        self,
        contest_id: int,
        interactor: Depends[GetStandings],
    ) -> schemas.StandingsSchema:
        standings, tasks = await interactor(contest_id)
        return schemas.StandingsSchema(
            tasks=[
                (task.type, task.id, task.title)
                for task in tasks
            ],
            table=[
                schemas.UserStandingsRowSchema(
                    user=schemas.UserSchema(
                        id=status.user.id,
                        username=status.user.username,
                        profile_pic=status.user.profile_pic,
                        roles=status.user.roles,
                    ),
                    tasks_attempted=status.tasks_attempted,
                    tasks_solved=status.tasks_solved,
                    solutions=status.solutions,
                    total_score=status.total_score,
                )
                for status in standings
            ],
        )


@get("/api/v1/solutions/ping/", exclude_from_auth=True)
@inject
async def ping() -> str:
    return "ok"
