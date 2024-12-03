"""Provides class for validating file output"""
from typing import override

from judgelet.compilers.abc_compiler import RunResult
from judgelet.exceptions import SerializationException
from judgelet.testing.validators.abc_validator import (AbstractValidator,
                                                       ValidatorAnswer,
                                                       ValidatorModel)

# TODO: consider moving away from package with abstractions


class FileValidator(AbstractValidator):
    """Validates file output"""

    def __init__(self, file_path: str, expected: str, apply_strip: bool | None = None):
        """Create file validator"""
        self.file_path = file_path
        self.expected = expected
        if apply_strip is None:
            apply_strip = True
        self.apply_strip = apply_strip

    @override
    def validate_run_result(self, run_result: RunResult) -> ValidatorAnswer:
        if self.file_path not in run_result.files:
            return ValidatorAnswer.err_presentation_error()
        output = run_result.files[self.file_path]
        if self.apply_strip:
            output = output.strip()
        if output == self.expected:
            return ValidatorAnswer.ok()
        return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    @override
    def deserialize(validator: ValidatorModel):
        if "file_path" not in validator.args:
            raise SerializationException
        if "expected" not in validator.args:
            raise SerializationException
        return FileValidator(
            str(validator.args["file_path"]),
            str(validator.args["expected"]),
            validator.args.get("apply_strip")
        )
