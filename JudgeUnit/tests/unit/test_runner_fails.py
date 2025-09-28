import pytest

from judgelet.domain.execution import LanguageBackend, SolutionRunner
from tests.unit.factory import create_group, create_suite, create_test
from tests.unit.fakes import (
    FakeCompileErrorCompiler,
    FakeCompileMemoryLimitCompiler, FakeCompileTimeLimitCompiler,
    FakeEmptySolution,
    FakeFileSystem,
    FakeRunMemoryLimitCompiler,
    FakePrepareErrorCompiler,
    FakeRunTimeLimitCompiler,
    FakeRuntimeErrorCompiler,
    FakeSandbox,
)


def _create_runner(compiler: LanguageBackend) -> SolutionRunner:
    fs = FakeFileSystem()
    return SolutionRunner(
        compiler,
        FakeEmptySolution(),
        fs,
        FakeSandbox(fs)
    )


@pytest.mark.parametrize(
    "compiler", [
        FakePrepareErrorCompiler(),
        FakeCompileErrorCompiler(),
        FakeCompileTimeLimitCompiler(),
        FakeCompileMemoryLimitCompiler()
    ]
)
@pytest.mark.asyncio
async def test_compile_fail(compiler):
    test_suite = create_suite()
    runner = _create_runner(compiler)
    result = await test_suite.run(runner)
    assert result.verdict.codename == "CE"


@pytest.mark.asyncio
async def test_runtime_fail():
    test_suite = create_suite(create_group("A", create_test()))
    runner = _create_runner(FakeRuntimeErrorCompiler())
    result = await test_suite.run(runner)
    assert result.verdict.codename == "RE"


@pytest.mark.asyncio
async def test_run_time_limit():
    test_suite = create_suite(create_group("A", create_test()))
    runner = _create_runner(FakeRunTimeLimitCompiler())
    result = await test_suite.run(runner)
    assert result.verdict.codename == "TL"


@pytest.mark.asyncio
async def test_run_memory_limit():
    test_suite = create_suite(create_group("A", create_test()))
    runner = _create_runner(FakeRunMemoryLimitCompiler())
    result = await test_suite.run(runner)
    assert result.verdict.codename == "ML"
