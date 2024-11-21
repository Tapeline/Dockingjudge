"""Provides class for validating file output"""

from judgelet.compilers.abc_compiler import RunResult
from judgelet.exceptions import SerializationException
from judgelet.testing.validators.abc_validator import Validator, ValidatorAnswer, ValidatorModel


class FileValidator(Validator):
    """Validates file output"""
    file_path: str
    expected: str
    apply_strip: bool = True

    def __init__(self, file_path: str, expected: str, apply_strip: bool | None = None):
        self.file_path = file_path
        self.expected = expected
        if apply_strip is None:
            apply_strip = True
        self.apply_strip = apply_strip

    def validate_run_result(self, result: RunResult) -> ValidatorAnswer:
        if self.file_path not in result.files:
            return ValidatorAnswer.err_presentation_error()
        output = result.files[self.file_path].strip() \
            if self.apply_strip else result.files[self.file_path]
        if output == self.expected:
            return ValidatorAnswer.ok()
        return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    def deserialize(validator: ValidatorModel):
        if "file_path" not in validator.args:
            raise SerializationException
        if "expected" not in validator.args:
            raise SerializationException
        return FileValidator(str(validator.args["file_path"]),
                             str(validator.args["expected"]),
                             validator.args.get("apply_strip"))
