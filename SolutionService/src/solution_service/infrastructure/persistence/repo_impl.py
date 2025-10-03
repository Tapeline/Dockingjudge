from typing import Sequence, override

import sqlalchemy
from sqlalchemy import delete, select, and_, or_, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from solution_service.application.interfaces import solutions
from solution_service.application.interfaces.solutions import (
    PaginationParameters,
    UserSolutionScore,
    UserStandingRow,
)
from solution_service.domain.abstract import (
    AnySolution,
    TaskType,
    CodeSolution,
    QuizSolution,
    SubmissionType,
)
from solution_service.infrastructure.persistence.models import SolutionModel


def _transform_solution_model_to_entity(
        model: SolutionModel | None
) -> AnySolution | None:
    if model is None:
        return None
    commons = {
        "uid": str(model.uuid),
        "contest_id": model.contest_id,
        "task_type": model.task_type,
        "task_id": model.task_id,
        "user_id": model.user_id,
        "score": model.score,
        "short_verdict": model.short_verdict,
        "submitted_at": model.submitted_at
    }
    if model.task_type == TaskType.CODE:
        return CodeSolution(
            detailed_verdict=model.detailed_verdict or "NC",
            group_scores=model.group_scores or {},
            submission_url=model.answer,
            main_file=model.main_file,
            compiler_name=model.compiler_name,
            submission_type=SubmissionType(
                model.code_solution_type
            ),
            **commons
        )
    if model.task_type == TaskType.QUIZ:
        return QuizSolution(
            submitted_answer=model.answer,
            **commons
        )
    raise TypeError(
        "Cannot transform solution model to entity: "
        "unexpected type " + str(model)
    )


def _select_contest_tasks(
        contest_tasks: Sequence[tuple[TaskType, int]]
) -> sqlalchemy.Select:
    quiz_tasks_filter = [
        task[1] for task in contest_tasks
        if task[0] == TaskType.QUIZ
    ]
    code_tasks_filter = [
        task[1] for task in contest_tasks
        if task[0] == TaskType.CODE
    ]
    return select(SolutionModel).filter(
        or_(
            and_(
                SolutionModel.task_type == TaskType.QUIZ,
                SolutionModel.task_id.in_(quiz_tasks_filter)
            ),
            and_(
                SolutionModel.task_type == TaskType.CODE,
                SolutionModel.task_id.in_(code_tasks_filter)
            )
        )
    )


def _apply_pagination(query, pagination: PaginationParameters):
    if pagination.offset is not None:
        query = query.offset(pagination.offset)
    if pagination.limit is not None:
        query = query.limit(pagination.limit)
    return query


class SolutionRepoImpl(solutions.SolutionRepository):
    # TODO: move .commit over to DBSession and application layer

    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def get_all_solutions_of_user(
            self,
            user_id: int,
            task_type: str | None = None,
            pagination_params: PaginationParameters | None = None
    ) -> list[AnySolution]:
        pagination_params = pagination_params or PaginationParameters()
        query = select(SolutionModel).filter(
            SolutionModel.user_id == user_id
        )
        query = _apply_pagination(query, pagination_params)
        models = await self._session.execute(query)
        return list(
            map(
                _transform_solution_model_to_entity,
                models.scalars().all()
            )
        )

    @override
    async def get_all_solutions_of_user_for_contest(
        self,
        user_id: int,
        contest_tasks: Sequence[tuple[TaskType, int]],
        pagination_params: PaginationParameters | None = None
    ) -> Sequence[AnySolution]:
        pagination_params = pagination_params or PaginationParameters()
        query = _select_contest_tasks(contest_tasks).filter(
            SolutionModel.user_id == user_id,
        )
        query = _apply_pagination(query, pagination_params)
        models = await self._session.execute(query)
        return list(
            map(
                _transform_solution_model_to_entity,
                models.scalars().all()
            )
        )

    @override
    async def get_all_solutions_of_task(
            self,
            user_id: int,
            task_type: TaskType,
            task_id: int,
            pagination_params: PaginationParameters | None = None
    ) -> list[AnySolution]:
        pagination_params = pagination_params or PaginationParameters()
        query = select(SolutionModel).filter(
            and_(
                SolutionModel.user_id == user_id,
                SolutionModel.task_type == task_type,
                SolutionModel.task_id == task_id
            )
        )
        query = _apply_pagination(query, pagination_params)
        models = await self._session.execute(query)
        return list(
            map(
                _transform_solution_model_to_entity,
                models.scalars().all()
            )
        )

    @override
    async def get_contest_standings(
        self,
        contest_tasks: Sequence[tuple[TaskType, int]],
        participants: Sequence[int]
    ) -> Sequence[UserStandingRow]:
        subquery = (
            select(
                SolutionModel.user_id,
                SolutionModel.task_type,
                SolutionModel.task_id,
                func.max(SolutionModel.score).label("best_score"),
            )
            .group_by(
                SolutionModel.user_id,
                SolutionModel.task_type,
                SolutionModel.task_id,
            )
            .subquery("s")
        )
        query = select(
            subquery.c.user_id,
            subquery.c.task_id,
            subquery.c.task_type,
            subquery.c.best_score,
            SolutionModel.uuid,
            SolutionModel.short_verdict
        ).join_from(
            subquery,
            SolutionModel,
            and_(
                SolutionModel.user_id == subquery.c.user_id,
                SolutionModel.task_id == subquery.c.task_id,
                SolutionModel.score == subquery.c.best_score,
            ),
        )
        statuses = {
            participant: UserStandingRow(
                solutions=[None] * len(contest_tasks),
                tasks_solved=0,
                tasks_attempted=0,
                total_score=0,
            )
            for participant in participants
        }
        best_solutions = await self._session.execute(query)
        for (
            user_id, task_id, task_type, score, solution_id, short_verdict
        ) in best_solutions:
            status = statuses[user_id]
            status.tasks_attempted += 1
            status.total_score += score
            status.tasks_solved += short_verdict.lower() == "ok"
            status.solutions[
                contest_tasks.index((task_type, task_id))
            ] = UserSolutionScore(
                task_type=TaskType(task_type),
                task_id=task_id,
                user_id=user_id,
                score=score
            )
        return [statuses[participant] for participant in participants]

    @override
    async def get_solution(self, solution_id: str) -> AnySolution | None:
        query = select(SolutionModel).filter(
            SolutionModel.uuid == solution_id
        )
        models = await self._session.execute(query)
        return _transform_solution_model_to_entity(models.scalars().one())

    @override
    async def get_best_solution_by_user_task(
            self,
            user_id: int,
            task_type: TaskType,
            task_id: int
    ) -> AnySolution | None:
        query = select(SolutionModel).filter(
            and_(
                SolutionModel.user_id == user_id,
                SolutionModel.task_type == task_type,
                SolutionModel.task_id == task_id
            )
        ).order_by(SolutionModel.score.desc())
        models = await self._session.execute(query)
        return _transform_solution_model_to_entity(models.scalars().first())

    @override
    async def create_solution(self, solution: AnySolution) -> None:
        answer = None
        group_scores = None
        detailed_verdict = None
        compiler_name = None
        main_file = None
        submission_type = None
        if isinstance(solution, QuizSolution):
            answer = solution.submitted_answer
        else:
            answer = solution.submission_url
            group_scores = solution.group_scores
            detailed_verdict = solution.detailed_verdict
            compiler_name = solution.compiler_name
            main_file = solution.main_file
            submission_type = solution.submission_type
        model = SolutionModel(
            uuid=solution.uid,
            contest_id=solution.contest_id,
            task_id=solution.task_id,
            task_type=solution.task_type,
            score=solution.score,
            short_verdict=solution.short_verdict,
            user_id=solution.user_id,
            answer=answer,
            group_scores=group_scores,
            detailed_verdict=detailed_verdict,
            compiler_name=compiler_name,
            main_file=main_file,
            code_solution_type=submission_type
        )
        self._session.add(model)

    @override
    async def store_solution_check_result(
        self,
        solution_id: str,
        score: int,
        detailed_verdict: str,
        short_verdict: str,
        group_scores: dict[str, int],
        protocol: dict,
    ) -> None:
        query = update(SolutionModel).where(SolutionModel.uuid == solution_id)
        query = query.values(
            score=score,
            short_verdict=short_verdict,
            detailed_verdict=detailed_verdict,
            group_scores=group_scores,
        )
        await self._session.execute(query)
        await self._session.commit()

    @override
    async def purge_user_solutions(self, user_id: int) -> None:
        await self._session.execute(
            delete(SolutionModel).where(SolutionModel.user_id == user_id)
        )
        await self._session.commit()

    @override
    async def purge_task_solutions(
            self,
            task_type: TaskType,
            task_id: int
    ) -> None:
        await self._session.execute(
            delete(SolutionModel).where(
                SolutionModel.task_id == task_id,
                SolutionModel.task_type == task_type
            )
        )
        await self._session.commit()
