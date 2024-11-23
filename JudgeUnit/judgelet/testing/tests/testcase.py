"""Provides classes for representing and running test cases"""

from judgelet.compilers.abc_compiler import AbstractCompiler, RunResult
from judgelet.testing.validators.abc_validator import AbstractValidator, ValidatorAnswer
from judgelet import models


class TestCase:
    """Represents a single test case"""
    validators: list[AbstractValidator]
    stdin_data: str
    files: dict[str, str]
    required_back_files: set[str]
    time_limit: int
    memory_limit_mb: int

    def __init__(self, validators: list[AbstractValidator], stdin_data: str,
                 files: dict[str, str], required_back_files: set[str],
                 time_limit: int, memory_limit_mb: int):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-positional-arguments
        self.validators = validators
        self.stdin_data = stdin_data
        self.files = files
        self.required_back_files = required_back_files
        self.time_limit = time_limit
        self.memory_limit_mb = memory_limit_mb

    async def perform_test_case(self, context, compiler_name: str, file_name: str,
                                solution_dir: str) -> tuple[RunResult, ValidatorAnswer]:
        """Run and validate output"""
        if compiler_name not in AbstractCompiler.COMPILERS:
            return ValidatorAnswer.err("Compiler not found")
        compiler = AbstractCompiler.COMPILERS[compiler_name](context)
        compiler_result = await compiler.launch_and_get_output(
            file_name, self.stdin_data, self.files,
            self.required_back_files, self.time_limit,
            self.memory_limit_mb, solution_dir
        )
        for validator in self.validators:
            validator_answer = validator.perform_full_validation(compiler_result)
            if not validator_answer.success:
                return compiler_result, validator_answer

        return compiler_result, ValidatorAnswer.ok()

    @staticmethod
    def deserialize(data: models.TestCase) -> "TestCase":
        """Create from pydantic"""
        validators = [AbstractValidator.deserialize(validator_data)
                      for validator_data in data.validators]
        return TestCase(
            validators,
            data.stdin,
            data.files_in,
            set(data.files_out),
            data.time_limit,
            data.mem_limit_mb
        )
