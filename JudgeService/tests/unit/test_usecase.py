import pytest

from judgeservice.application.interactors import ProcessSolutionInteractor
from tests.unit.factory import (
    SolutionFactory,
    create_judgelets,
    create_simple_pool,
)
from tests.unit.fakes import FakeSolutionGateway


@pytest.mark.asyncio
async def test_solution_processed():
    interactor = ProcessSolutionInteractor(
        judgelet_pool=create_simple_pool(
            create_judgelets([{"address": "a"}]),
        ),
        solution_gateway=FakeSolutionGateway({"/test": b"Test solution"}),
    )
    solution = SolutionFactory().build(solution_url="/test")
    await interactor(solution)
    assert solution.short_verdict == "OK"
