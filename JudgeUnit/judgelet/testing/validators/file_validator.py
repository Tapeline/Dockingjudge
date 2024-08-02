from judgelet.compilers.abc_compiler import RunResult
from judgelet.exceptions import SerializationException
from judgelet.testing.validators.abc_validator import Validator, ValidatorAnswer, ValidatorModel


class FileValidator(Validator):
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
        output = result.files[self.file_path].strip() if self.apply_strip else result.files[self.file_path]
        if output == self.expected:
            return ValidatorAnswer.ok()
        else:
            return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    def deserialize(data: ValidatorModel):
        if "file_path" not in data.args:
            raise SerializationException
        if "expected" not in data.args:
            raise SerializationException
        return FileValidator(str(data.args["file_path"]),
                             str(data.args["expected"]),
                             data.args.get("apply_strip"))
