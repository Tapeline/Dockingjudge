from judgelet.compilers.abc_compiler import RunResult
from judgelet.exceptions import SerializationException
from judgelet.testing.validators.abc_validator import Validator, ValidatorAnswer, ValidatorModel


class StdoutValidator(Validator):
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
        else:
            return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    def deserialize(data: ValidatorModel):
        if "expected" not in data.args:
            raise SerializationException
        return StdoutValidator(str(data.args["expected"]), data.args.get("apply_strip"))
