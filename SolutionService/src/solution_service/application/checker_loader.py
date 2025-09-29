from typing import Generic

from solution_service.domain.entities.abstract import AbstractQuizChecker


class BadCheckerParametersException(Exception):
    """Thrown when parameters in loader are malformed"""


def _get_param_class(checker_class: type[AbstractQuizChecker]) -> type | None:
    return checker_class.__annotations__.get("params")


def load_checker(
        checker_type: str,
        checker_params: dict,
        max_score: int,
) -> AbstractQuizChecker | None:
    if checker_type not in AbstractQuizChecker.all_checkers:
        return None
    checker_class: type[AbstractQuizChecker] = AbstractQuizChecker.all_checkers[checker_type]
    param_class = _get_param_class(checker_class)
    if param_class is None:
        return checker_class(max_score, checker_params)
    try:
        params = param_class(**checker_params)
    except TypeError as arg_exception:
        raise BadCheckerParametersException from arg_exception
    checker = checker_class(max_score, params)
    return checker
