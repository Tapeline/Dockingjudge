from typing import Any

# important, do not remove
from solution_service.domain import quiz_checkers  # noqa: F401
from solution_service.domain.abstract import AbstractQuizChecker


class BadCheckerParametersException(Exception):
    """Thrown when parameters in loader are malformed."""


def load_checker(
    checker_type: str,
    checker_params: dict[str, Any],
    max_score: int,
) -> AbstractQuizChecker[Any] | None:
    """Instantiate checker of a specific type."""
    if checker_type not in AbstractQuizChecker.all_checkers:
        return None
    checker_class = AbstractQuizChecker.all_checkers[checker_type]
    param_class = _get_param_class(checker_class)
    if param_class is None:
        return checker_class(max_score, checker_params)
    try:
        params = param_class(**checker_params)
    except TypeError as arg_exception:
        raise BadCheckerParametersException from arg_exception
    return checker_class(max_score, params)


def _get_param_class(
    checker_class: type[AbstractQuizChecker[Any]],
) -> type | None:
    return checker_class.__annotations__.get("params")
