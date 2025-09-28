from typing import Any, Final

import pytest

from judgelet.application.precompile_checkers import (
    HasPatternChecker, NoImportChecker,
    NoPatternChecker,
)
from judgelet.domain.checking import NoArgs
from tests.unit.fakes import FakeFileSystem


_SHOULD_PASS: Final = True
_SHOULD_FAIL: Final = False


@pytest.mark.parametrize(
    ("src", "should_pass"),
    [
        ("import x", _SHOULD_FAIL),
        ("print('Hello, World!')", _SHOULD_PASS),
        ("print('import')", _SHOULD_PASS),
    ]
)
@pytest.mark.parametrize(
    "filename", ["test.py"]
)
def test_no_import(src: str, filename: str, should_pass: bool):
    fs = FakeFileSystem({filename: src})
    verdict = NoImportChecker(NoArgs()).check(fs, filename)
    assert verdict.is_successful == should_pass


@pytest.mark.parametrize(
    ("src", "checker_params", "should_pass"),
    [
        (
            "pattern",
            NoPatternChecker.args_cls(
                patterns={"py": ["pattern"]}
            ),
            _SHOULD_FAIL
        ),
        (
            "nnnneedle",
            NoPatternChecker.args_cls(
                patterns={"py": ["n+eedle"]}
            ),
            _SHOULD_FAIL
        ),
        (
            "doesn't match",
            NoPatternChecker.args_cls(
                patterns={"py": ["pattern"]}
            ),
            _SHOULD_PASS
        ),
    ]
)
@pytest.mark.parametrize(
    "filename", ["test.py"]
)
def test_no_pattern(
    src: str,
    checker_params: Any,
    filename: str,
    should_pass: bool
):
    fs = FakeFileSystem({filename: src})
    verdict = NoPatternChecker(checker_params).check(fs, filename)
    assert verdict.is_successful == should_pass


@pytest.mark.parametrize(
    ("src", "checker_params", "should_pass"),
    [
        (
            "pattern",
            HasPatternChecker.args_cls(
                patterns={"py": ["pattern"]}
            ),
            _SHOULD_PASS
        ),
        (
            "nnnneedle",
            HasPatternChecker.args_cls(
                patterns={"py": ["n+eedle"]}
            ),
            _SHOULD_PASS
        ),
        (
            "doesn't match",
            HasPatternChecker.args_cls(
                patterns={"py": ["pattern"]}
            ),
            _SHOULD_FAIL
        ),
    ]
)
@pytest.mark.parametrize(
    "filename", ["test.py"]
)
def test_has_pattern(
    src: str,
    checker_params: Any,
    filename: str,
    should_pass: bool
):
    fs = FakeFileSystem({filename: src})
    verdict = HasPatternChecker(checker_params).check(fs, filename)
    assert verdict.is_successful == should_pass


def test_pattern_does_not_match_unknown_extensions():
    fs = FakeFileSystem({"test.unknown": "import x"})
    verdict = NoImportChecker(NoArgs()).check(fs, "test.unknown")
    assert verdict.is_successful
