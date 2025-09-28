from types import MappingProxyType
from typing import Final, Mapping, override

from pydantic import BaseModel

from judgelet.domain.checking import Validator
from judgelet.domain.results import RunResult, Verdict
from judgelet.domain.test_case import TestCase


class _StdoutValidatorArgs(BaseModel):
    expected: str
    strip: bool = True


class StdoutValidator(Validator[_StdoutValidatorArgs]):
    """Validates stdout."""

    args_cls = _StdoutValidatorArgs

    @override
    def validate(
        self,
        result: RunResult,
        test_case: TestCase,
        output_files: Mapping[str, str]
    ) -> Verdict:
        actual = result.stdout
        expected = self.args.expected
        if self.args.strip:
            actual = actual.strip()
            expected = expected.strip()
        if actual != expected:
            return Verdict.WA()
        return Verdict.OK()


class _FileValidatorArgs(BaseModel):
    filename: str
    expected: str
    strip: bool = True


class FileValidator(Validator[_FileValidatorArgs]):
    """Validates files contents."""

    args_cls = _FileValidatorArgs

    @override
    def validate(
        self,
        result: RunResult,
        test_case: TestCase,
        output_files: Mapping[str, str]
    ) -> Verdict:
        if self.args.filename not in output_files:
            return Verdict.PE(f"file {self.args.filename} not found")
        actual = output_files[self.args.filename]
        expected = self.args.expected
        if self.args.strip:
            actual = actual.strip()
            expected = expected.strip()
        if actual != expected:
            return Verdict.WA()
        return Verdict.OK()


VALIDATORS: Final = MappingProxyType({
    "stdout": StdoutValidator,
    "file": FileValidator
})
