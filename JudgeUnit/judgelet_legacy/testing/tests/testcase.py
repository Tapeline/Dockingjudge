"""Provides classes for representing and running test cases"""

from judgelet import models
from judgelet.compilers.abc_compiler import AbstractCompiler, RunResult
from judgelet.testing.validators.abc_validator import (AbstractValidator,
                                                       ValidatorAnswer)


class TestCase:
    """Represents a single test case"""

    def __init__(  # noqa: WPS211 (too many args)
            self,
            validators: list[AbstractValidator],
            stdin_data: str,
            files: dict[str, str],
            required_back_files: set[str],
            time_limit: int | None,
            memory_limit_mb: int | None
    ):
        """Create test case"""
        self.validators = validators
        self.stdin_data = stdin_data
        self.files = files
        self.required_back_files = required_back_files
        self.time_limit = time_limit
        self.memory_limit_mb = memory_limit_mb

    async def perform_test_case(
            self,
            context,
            compiler_name: str,
            file_name: str,
            solution_dir: str
    ) -> tuple[RunResult, ValidatorAnswer]:
        """Run and validate output"""
        if compiler_name not in AbstractCompiler.COMPILERS:
            return ValidatorAnswer.err("Compiler not found")
        compiler = AbstractCompiler.COMPILERS[compiler_name](context)
        compiler_result = await compiler.launch_and_get_output(
            file_name,
            self.stdin_data,
            self.files,
            self.required_back_files,
            self.time_limit,
            self.memory_limit_mb,
            solution_dir
        )
        for validator in self.validators:
            validator_answer = validator.perform_full_validation(compiler_result)
            if not validator_answer.success:
                return compiler_result, validator_answer

        return compiler_result, ValidatorAnswer.ok()

    @staticmethod
    def deserialize(model: models.TestCase) -> "TestCase":
        """Create from pydantic"""
        validators = [AbstractValidator.deserialize(validator_data)
                      for validator_data in model.validators]
        return TestCase(
            validators,
            model.stdin,
            model.files_in,
            set(model.files_out),
            model.time_limit,
            model.mem_limit_mb
        )
