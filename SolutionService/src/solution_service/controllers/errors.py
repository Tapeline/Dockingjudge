from typing import Final

from solution_service.application.exceptions import (
    MayNotAccessSolution,
    MayNotSubmitSolution,
    NotAuthenticated,
    NotFound,
)
from solution_service.controllers.error_commons import (
    gen_handler_mapping,
    infer_code,
)
from solution_service.infrastructure.exceptions import (
    BadServiceResponseException,
)

handlers: Final = gen_handler_mapping({
    NotFound: (404, infer_code),
    MayNotAccessSolution: (403, infer_code),
    BadServiceResponseException: (500, "bad_dependency_response"),
    NotAuthenticated: (401, infer_code),
    MayNotSubmitSolution: (403, infer_code),
})
