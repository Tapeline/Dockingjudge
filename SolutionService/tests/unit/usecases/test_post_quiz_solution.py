
import pytest

from solution_service.application.exceptions import (
    MayNotSubmitSolution,
)
from solution_service.application.interactors.post_quiz_solution import (
    PostQuizSolution,
)
from solution_service.application.interfaces.contest import ValidatorDTO

# important, do not remove
from solution_service.domain import quiz_checkers  # noqa
from tests.unit.factory import (
    NewQuizSolutionFactory,
    QuizTaskFactory,
    UserFactory,
)
from tests.unit.fakes import (
    FakeContestService,
    FakeUserIdP,
)


@pytest.mark.parametrize(
    ("answer", "validator", "verdict"),
    [
        (
            "Apple",
            ValidatorDTO(
                type="text",
                args=dict(
                    pattern="Apple",
                ),
            ),
            "OK",
        ),
        (
            "apppppppple",
            ValidatorDTO(
                type="regex",
                args=dict(
                    pattern="app+le",
                ),
            ),
            "OK",
        ),
        (
            "aple",
            ValidatorDTO(
                type="regex",
                args=dict(
                    pattern="app+le",
                ),
            ),
            "WA",
        ),
    ],
)
@pytest.mark.asyncio
async def test_solution_posting(
    post_quiz_solution_interactor: PostQuizSolution,
    user_factory: UserFactory,
    fake_user_idp: FakeUserIdP,
    new_quiz_solution_factory: NewQuizSolutionFactory,
    fake_contest_service: FakeContestService,
    quiz_task_factory: QuizTaskFactory,
    answer: str,
    validator: ValidatorDTO,
    verdict: str,
):
    user = user_factory.build()
    fake_user_idp.user = user
    new_solution = new_quiz_solution_factory.build(text=answer)
    fake_contest_service.quiz_tasks[new_solution.task_id] = (
        quiz_task_factory.build(validator=validator)
    )

    posted_solution = await post_quiz_solution_interactor(new_solution)

    assert posted_solution.submitted_answer == new_solution.text
    assert posted_solution.short_verdict == verdict


@pytest.mark.asyncio
async def test_cannot_post_solution_if_contest_svc_says_so(
    post_quiz_solution_interactor: PostQuizSolution,
    user_factory: UserFactory,
    fake_user_idp: FakeUserIdP,
    new_quiz_solution_factory: NewQuizSolutionFactory,
    fake_contest_service: FakeContestService,
    quiz_task_factory: QuizTaskFactory,
):
    user = user_factory.build()
    fake_user_idp.user = user
    new_solution = new_quiz_solution_factory.build()
    fake_contest_service.quiz_tasks[new_solution.task_id] = (
        quiz_task_factory.build()
    )
    fake_contest_service.can_submit_task = False

    with pytest.raises(MayNotSubmitSolution):
        await post_quiz_solution_interactor(new_solution)
