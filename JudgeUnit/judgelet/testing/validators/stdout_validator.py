"""Provides class for validating stdout"""

from judgelet.compilers.abc_compiler import RunResult
from judgelet.exceptions import SerializationException
from judgelet.testing.validators.abc_validator import AbstractValidator, ValidatorAnswer, ValidatorModel


class StdoutValidator(AbstractValidator):
    """Validates stdout"""
    expected: str
    apply_strip: bool = True

    def __init__(self, expected: str, apply_strip: bool | None = None):
        self.expected = expected
        if apply_strip is None:
            apply_strip = True
        self.apply_strip = apply_strip

    def validate_run_result(self, result: RunResult) -> ValidatorAnswer:
        output = result.stdout.strip() if self.apply_strip else result.stdout
        expected = self.expected.strip() if self.apply_strip else self.expected
        if output == expected:
            return ValidatorAnswer.ok()
        return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    def deserialize(validator: ValidatorModel):
        if "expected" not in validator.args:
            raise SerializationException
        return StdoutValidator(str(validator.args["expected"]),
                               validator.args.get("apply_strip"))
