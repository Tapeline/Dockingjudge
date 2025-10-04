from typing import Any

import pytest

from solution_service.application.exceptions import (
    MayNotSubmitSolution,
)
from solution_service.application.interactors.post_code_solution import (
    PostCodeSolution,
)
from solution_service.domain.abstract import SubmissionType
from tests.unit.factory import (
    CodeTaskFactory,
    NewCodeSolutionFactory,
    UserFactory,
    from_base64,
    to_base64,
)
from tests.unit.fakes import (
    FakeContestService,
    FakeObjectStore,
    FakeSolutionPublisher,
    FakeUserIdP,
)


@pytest.mark.parametrize(
    "solution_params",
    [
        {
            "submission_type": SubmissionType.STR,
            "text": "print('Hello, World')",
            "main_file": None,
        },
        {
            "submission_type": SubmissionType.ZIP,
            "text": to_base64("some zip content"),
            "main_file": "main.py",
        },
    ],
)
@pytest.mark.asyncio
async def test_code_solution_posting(
    post_code_solution_interactor: PostCodeSolution,
    user_factory: UserFactory,
    fake_user_idp: FakeUserIdP,
    new_code_solution_factory: NewCodeSolutionFactory,
    fake_contest_service: FakeContestService,
    solution_params: dict[str, Any],
    code_task_factory: CodeTaskFactory,
    fake_solution_publisher: FakeSolutionPublisher,
    fake_object_store: FakeObjectStore,
):
    user = user_factory.build()
    fake_user_idp.user = user
    new_solution = new_code_solution_factory.build(**solution_params)
    fake_contest_service.code_tasks[new_solution.task_id] = (
        code_task_factory.build()
    )

    posted_solution = await post_code_solution_interactor(new_solution)

    file = await fake_object_store.get_file(posted_solution.submission_url)
    if solution_params["submission_type"] == SubmissionType.ZIP:
        assert file.str_contents == from_base64(solution_params["text"])
    else:
        assert file.str_contents == solution_params["text"]
    assert fake_solution_publisher.published[0][0] == posted_solution


@pytest.mark.asyncio
async def test_cannot_post_solution_if_contest_svc_says_so(
    post_code_solution_interactor: PostCodeSolution,
    user_factory: UserFactory,
    fake_user_idp: FakeUserIdP,
    new_code_solution_factory: NewCodeSolutionFactory,
    fake_contest_service: FakeContestService,
    code_task_factory: CodeTaskFactory,
):
    user = user_factory.build()
    fake_user_idp.user = user
    new_solution = new_code_solution_factory.build()
    fake_contest_service.code_tasks[new_solution.task_id] = (
        code_task_factory.build()
    )
    fake_contest_service.can_submit_task = False

    with pytest.raises(MayNotSubmitSolution):
        await post_code_solution_interactor(new_solution)
