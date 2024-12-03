from judgelet import models
from judgelet.compilers.abc_compiler import (AbstractCompiler, RunResult,
                                             UtilityRunResult)
from judgelet.compilers.default_compiler import DefaultCompiler
from judgelet.models import ScoringRuleEnum
from judgelet.models import Validator as ValidatorModel
from judgelet.sandbox.sandbox import Sandbox, SandboxExitCause, SandboxResult
from judgelet.testing.tests.testsuite import TestSuite
from judgelet.testing.validators.abc_validator import (AbstractValidator,
                                                       ValidatorAnswer)


class MockCompiler(DefaultCompiler):
    async def test_impl(self, file_path: str, proc_input: str, timeout: float, mem_limit_mb: float,
                        sandbox: Sandbox) -> SandboxResult:
        return SandboxResult(0, SandboxExitCause.PROCESS_EXITED, "", "")

    async def prepare(self, file_path: str, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()

    async def compile(self, file_path: str, compile_timeout, solution_dir) -> UtilityRunResult:
        return UtilityRunResult.ok()


class MockOkValidator(AbstractValidator):

    def validate_run_result(self, run_result: RunResult) -> ValidatorAnswer:
        return ValidatorAnswer.ok()

    @staticmethod
    def deserialize(validator: ValidatorModel):
        return MockOkValidator()


class MockWAValidator(AbstractValidator):
    def validate_run_result(self, run_result: RunResult) -> ValidatorAnswer:
        return ValidatorAnswer.err_wrong_answer()

    @staticmethod
    def deserialize(validator: ValidatorModel):
        return MockWAValidator()


AbstractCompiler.COMPILERS["mock"] = MockCompiler
AbstractValidator.VALIDATORS["mock_ok"] = MockOkValidator
AbstractValidator.VALIDATORS["mock_wa"] = MockWAValidator


def _default_test_suite(case_validators: list[dict],
                        score: int,
                        scoring_rule=ScoringRuleEnum.GRADED):
    return TestSuite.deserialize(models.TestSuite(
        precompile=[],
        groups=[
            models.TestGroup(
                name="A",
                points=100,
                scoring_rule=scoring_rule,
                cases=[
                    models.TestCase(
                        validators=[models.Validator(**validator)],
                        stdin=""
                    ) for validator in case_validators
                ]
            )
        ],
        time_limit=1,
        mem_limit_mb=256
    ))


async def test_all_ok():
    suite = _default_test_suite([
        {"type": "mock_ok", "args": {}},
        {"type": "mock_ok", "args": {}}
    ], score=100)
    result = await suite.run_suite("mock", "", "", [])
    assert result.verdict == "OK"
    assert result.score == 100


async def test_wrong_answer_on_graded():
    suite = _default_test_suite([
        {"type": "mock_ok", "args": {}},
        {"type": "mock_wa", "args": {}}
    ], score=100)
    result = await suite.run_suite("mock", "", "", [])
    assert result.verdict == "WA"
    assert result.score == 50


async def test_wrong_answer_on_polar():
    suite = _default_test_suite([
        {"type": "mock_ok", "args": {}},
        {"type": "mock_wa", "args": {}}
    ], score=100, scoring_rule=ScoringRuleEnum.POLAR)
    result = await suite.run_suite("mock", "", "", [])
    assert result.verdict == "WA"
    assert result.score == 0


async def test_fail_dependency():
    suite = TestSuite.deserialize(models.TestSuite(
        precompile=[],
        groups=[
            models.TestGroup(
                name="A1",
                points=100,
                cases=[
                    models.TestCase(
                        validators=[models.Validator(type="mock_ok", args={})],
                        stdin=""
                    ),
                    models.TestCase(
                        validators=[models.Validator(type="mock_wa", args={})],
                        stdin=""
                    )
                ]
            ),
            models.TestGroup(
                name="B1",
                points=100,
                depends_on=["A1"],
                cases=[
                    models.TestCase(
                        validators=[models.Validator(type="mock_ok", args={})],
                        stdin=""
                    ),
                    models.TestCase(
                        validators=[models.Validator(type="mock_ok", args={})],
                        stdin=""
                    )
                ]
            )
        ],
        time_limit=1,
        mem_limit_mb=256
    ))
    result = await suite.run_suite("mock", "", "", [])
    assert result.verdict == "WA"
    assert result.score == 50
