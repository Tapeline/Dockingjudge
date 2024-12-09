import uuid
from typing import Callable, TypedDict

import pytest

from judgelet.models import RunRequest

TestSuiteDataFactory = Callable[[str, str, list[dict]], RunRequest]


@pytest.fixture(scope="package")
def test_suite_data_factory() -> TestSuiteDataFactory:
    def factory(compiler, code, groups, **additional) -> RunRequest:
        return RunRequest(**{
            "id": str(uuid.uuid4()),
            "compiler": compiler,
            "code": {
                "type": "string",
                "code": code
            },
            "suite": {
                "precompile": [],
                "groups": groups,
                "time_limit": 1,
                "mem_limit_mb": 256,
                **additional
            }
        })

    return factory


class StdoutValidationCase(TypedDict):
    stdin: str
    stdout: str


def create_group_with_stdout_validation(
        name: str,
        cases: list[StdoutValidationCase],
        *,
        depends_on: list[str] | None = None,
        score: int = 100,
        scoring_rule: str = "graded"
):
    if depends_on is None:
        depends_on = []
    return {
        "name": name,
        "points": score,
        "scoring_rule": scoring_rule,
        "depends_on": depends_on,
        "cases": [
            {
                "validators": [{"type": "stdout", "args": {"expected": case["stdout"]}}],
                "stdin": case["stdin"],
                "files_in": {},
                "files_out": []
            }
            for case in cases
        ]
    }
