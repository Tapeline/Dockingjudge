from abc import abstractmethod

from judgelet.compilers.abc_compiler import RunResult, RunVerdict
from judgelet.exceptions import SerializationException
from judgelet.models import Validator as ValidatorModel


class ValidatorAnswer:
    success: bool
    message: str

    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message

    def to_dict(self):
        return {"success": self.success, "message": self.message}

    @classmethod
    def ok(cls):
        return ValidatorAnswer(True, "OK")

    @classmethod
    def err(cls, message: str):
        return ValidatorAnswer(False, message)

    @classmethod
    def err_wrong_answer(cls):
        return ValidatorAnswer(False, "WA")

    @classmethod
    def err_presentation_error(cls):
        return ValidatorAnswer(False, "PE")

    @classmethod
    def err_runtime_error(cls):
        return ValidatorAnswer(False, "RE")

    @classmethod
    def err_time_limit(cls):
        return ValidatorAnswer(False, "TL")

    @classmethod
    def err_mem_limit(cls):
        return ValidatorAnswer(False, "ML")


class Validator:
    VALIDATORS: dict[str, type["Validator"]] = {}

    def perform_error_check(self, result: RunResult) -> ValidatorAnswer | None:
        if result.verdict == RunVerdict.TL:
            return ValidatorAnswer.err_time_limit()
        if result.verdict == RunVerdict.ML:
            return ValidatorAnswer.err_mem_limit()
        if result.verdict == RunVerdict.REQUIRED_FILE_NOT_FOUND:
            return ValidatorAnswer.err_presentation_error()
        if result.return_code != 0:
            return ValidatorAnswer.err_runtime_error()
        return None

    @abstractmethod
    def validate_run_result(self, result: RunResult) -> ValidatorAnswer:
        raise NotImplementedError

    def perform_full_validation(self, result: RunResult) -> ValidatorAnswer:
        pre_check_result = self.perform_error_check(result)
        if pre_check_result is not None:
            return pre_check_result
        return self.validate_run_result(result)

    @staticmethod
    def deserialize(validator: ValidatorModel):
        if validator.type not in Validator.VALIDATORS:
            raise SerializationException("Validator not found")
        cls = Validator.VALIDATORS[validator.type]
        return cls.deserialize(validator)


def register_default_validators():
    from judgelet.testing.validators.file_validator import FileValidator
    from judgelet.testing.validators.stdout_validator import StdoutValidator
    Validator.VALIDATORS["stdout"] = StdoutValidator
    Validator.VALIDATORS["file"] = FileValidator


