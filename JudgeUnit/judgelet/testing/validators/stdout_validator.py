"""Provides class for validating stdout"""
from typing import override

from judgelet.compilers.abc_compiler import RunResult
from judgelet.exceptions import SerializationException
from judgelet.testing.validators.abc_validator import (AbstractValidator,
                                                       ValidatorAnswer,
                                                       ValidatorModel)

# TODO: consider moving away from package with abstractions


class StdoutValidator(AbstractValidator):
    """Validates stdout"""

    def __init__(self, expected: str, apply_strip: bool | None = None):
        """Create stdout validator"""
        self.expected = expected
        if apply_strip is None:
            apply_strip = True
        self.apply_strip = apply_strip

    @override
    def validate_run_result(self, run_result: RunResult) -> ValidatorAnswer:
        output = run_result.stdout.strip() if self.apply_strip else run_result.stdout
        expected = self.expected.strip() if self.apply_strip else self.expected
        if output == expected:
            return ValidatorAnswer.ok()
        return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    @override
    def deserialize(validator: ValidatorModel):
        if "expected" not in validator.args:
            raise SerializationException
        return StdoutValidator(
            str(validator.args["expected"]),
            validator.args.get("apply_strip")
        )
