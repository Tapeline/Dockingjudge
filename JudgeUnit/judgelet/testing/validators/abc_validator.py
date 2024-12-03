"""Provides classes and functions for validating output"""

from abc import ABC, abstractmethod

from judgelet import settings
from judgelet.class_loader import load_class
from judgelet.compilers.abc_compiler import RunResult, RunVerdict
from judgelet.exceptions import SerializationException
from judgelet.models import Validator as ValidatorModel


class ValidatorAnswer:  # noqa: WPS214 (too many methods)
    """Checking result"""

    def __init__(self, success: bool, message: str):
        """Create answer"""
        self.success = success
        self.message = message

    def to_dict(self):
        """Serialize"""
        return {"success": self.success, "message": self.message}

    @classmethod
    def ok(cls):
        """OK checker message"""
        return ValidatorAnswer(success=True, message="OK")

    @classmethod
    def err(cls, message: str):
        """Error checker message"""
        return ValidatorAnswer(success=False, message=message)

    @classmethod
    def err_wrong_answer(cls):
        """WA checker message"""
        return ValidatorAnswer(success=False, message="WA")

    @classmethod
    def err_presentation_error(cls):
        """PE checker message"""
        return ValidatorAnswer(success=False, message="PE")

    @classmethod
    def err_runtime_error(cls):
        """RE checker message"""
        return ValidatorAnswer(success=False, message="RE")

    @classmethod
    def err_time_limit(cls):
        """TL checker message"""
        return ValidatorAnswer(success=False, message="TL")

    @classmethod
    def err_mem_limit(cls):
        """ML checker message"""
        return ValidatorAnswer(success=False, message="ML")


class AbstractValidator(ABC):
    """Represents a validator"""

    VALIDATORS: dict[str, type["AbstractValidator"]] = {}

    def perform_error_check(self, run_result: RunResult) -> ValidatorAnswer | None:
        """Convert RunResult to answer"""
        if run_result.verdict == RunVerdict.TL:
            return ValidatorAnswer.err_time_limit()
        if run_result.verdict == RunVerdict.ML:
            return ValidatorAnswer.err_mem_limit()
        if run_result.verdict == RunVerdict.REQUIRED_FILE_NOT_FOUND:
            return ValidatorAnswer.err_presentation_error()
        if run_result.return_code != 0:
            return ValidatorAnswer.err_runtime_error()
        return None

    def perform_full_validation(self, run_result: RunResult) -> ValidatorAnswer:
        """Validate run result (including pre-validation errors)"""
        pre_check_result = self.perform_error_check(run_result)
        if pre_check_result is not None:
            return pre_check_result
        return self.validate_run_result(run_result)

    @abstractmethod
    def validate_run_result(self, run_result: RunResult) -> ValidatorAnswer:
        """Validate single program run output"""
        raise NotImplementedError

    @staticmethod
    def deserialize(validator: ValidatorModel):
        """Create from pydantic"""
        if validator.type not in AbstractValidator.VALIDATORS:
            raise SerializationException("Validator not found")
        validator_class = AbstractValidator.VALIDATORS[validator.type]
        return validator_class.deserialize(validator)


def register_default_validators():
    """Dependency injection mechanism"""
    for validator_name, validator_module in settings.VALIDATORS.items():
        AbstractValidator.VALIDATORS[validator_name] = load_class(
            validator_module, AbstractValidator
        )
