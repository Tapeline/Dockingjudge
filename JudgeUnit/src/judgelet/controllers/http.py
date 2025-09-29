from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, HttpMethod, route
from litestar.exceptions import ValidationException
from structlog import get_logger

from judgelet.application.interactors import CheckSolutionInteractor
from judgelet.controllers.schemas.dumping import dump_run_response
from judgelet.controllers.schemas.loading import load_solution, load_suite
from judgelet.controllers.schemas.request import RunRequest
from judgelet.controllers.schemas.response import RunResponse
from judgelet.infrastructure.languages.lang_list import LANGUAGES


class SolutionsController(Controller):
    """Main HTTP endpoints."""

    @route(
        http_method=HttpMethod.GET,
        path="/ping",
    )
    async def ping(self) -> str:
        """Healthcheck."""
        return "ok"

    @route(
        http_method=HttpMethod.POST,
        path="/run",
    )
    @inject
    async def run_solution(
        self,
        data: RunRequest,
        interactor: FromDishka[CheckSolutionInteractor],
    ) -> RunResponse:
        """Run solution against specified tests."""
        log = get_logger().bind(solution_id=data.id)
        if data.compiler not in LANGUAGES:
            raise ValidationException(
                f"bad compiler, avaliable: {LANGUAGES.keys()}",
            )
        test_suite = load_suite(data)
        solution = load_solution(data)
        log.info("Begin processing soluton")
        result = await interactor(data.compiler, solution, test_suite)
        return dump_run_response(result)
