from typing import Any, Final

import pytest

from judgelet.application.validators import FileValidator, StdoutValidator
from judgelet.domain.files import File
from judgelet.domain.results import RunResult
from tests.unit.factory import create_ok_result, create_test


_SHOULD_PASS: Final = True
_SHOULD_FAIL: Final = False
_TEST_CASE = create_test()


@pytest.mark.parametrize(
    ("result", "validator_params", "should_pass"),
    [
        (
            create_ok_result("apple"),
            StdoutValidator.args_cls(
                expected="apple"
            ),
            _SHOULD_PASS
        ),
        (
            create_ok_result("banana"),
            StdoutValidator.args_cls(
                expected="apple"
            ),
            _SHOULD_FAIL
        ),
        (
            create_ok_result("  \t\napple \n\n"),
            StdoutValidator.args_cls(
                expected="apple", strip=True
            ),
            _SHOULD_PASS
        ),
    ]
)
def test_stdout_validator(
    result: RunResult,
    validator_params: Any,
    should_pass: bool
):
    verdict = StdoutValidator(validator_params).validate(
        result, _TEST_CASE, {}
    )
    assert verdict.is_successful == should_pass


@pytest.mark.parametrize(
    ("file", "validator_params", "should_pass"),
    [
        (
            File("ans", "apple"),
            FileValidator.args_cls(
                filename="ans",
                expected="apple"
            ),
            _SHOULD_PASS
        ),
        (
            File("ans", "banana"),
            FileValidator.args_cls(
                filename="ans",
                expected="apple"
            ),
            _SHOULD_FAIL
        ),
        (
            File("ans", "  \t\napple \n\n"),
            FileValidator.args_cls(
                filename="ans",
                expected="apple",
                strip=True
            ),
            _SHOULD_PASS
        ),
        (
            File("ans", "apple"),
            FileValidator.args_cls(
                filename="missing",
                expected="apple"
            ),
            _SHOULD_FAIL
        ),
    ]
)
def test_file_validator(
    file: File,
    validator_params: Any,
    should_pass: bool
):
    verdict = FileValidator(validator_params).validate(
        RunResult.blank_ok(), _TEST_CASE, {file.name: file.contents}
    )
    assert verdict.is_successful == should_pass
