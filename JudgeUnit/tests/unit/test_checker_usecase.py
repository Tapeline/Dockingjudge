import pytest

from judgelet.application.interactors import CheckSolutionInteractor
from judgelet.domain.results import Verdict
from judgelet.domain.test_case import TestCase
from tests.unit.factory import create_group, create_suite, create_test
from tests.unit.fakes import (
    FakeCompilerFactory,
    FakeCompilerWorksOnlyIfFilePresent,
    FakeCompilerWorksOnlyIfFilePresentInRuntime,
    FakeEmptySolution,
    FakeFileSystem,
    FakeOkCompiler,
    FakeOkValidator,
    FakeSandboxFactory,
    FakeWrongAnswerValidator,
)


@pytest.mark.parametrize(
    ("tests", "expected_result"),
    [
        (
            [
                create_test(FakeOkValidator())
            ],
            (Verdict.OK(), 100)
        ),
        (
            [
                create_test(FakeOkValidator()),
                create_test(FakeWrongAnswerValidator())
            ],
            (Verdict.WA(), 50)
        ),
    ]
)
@pytest.mark.asyncio
async def test_interactor_returns(
    tests: list[TestCase], expected_result: tuple[str, int]
):
    interactor = CheckSolutionInteractor(
        backend_factory=FakeCompilerFactory(FakeOkCompiler),
        fs=FakeFileSystem(),
        sandbox_factory=FakeSandboxFactory()
    )
    result = await interactor(
        backend_name="doesn't matter now",
        solution=FakeEmptySolution(),
        test_suite=create_suite(
            create_group("A", *tests)
        )
    )
    expected_verdict, expected_score = expected_result
    assert result.score == expected_score
    assert result.verdict == expected_verdict


@pytest.mark.parametrize(
    "additional_files",
    [
        {},
        {"some_file.py": "some content"},
        {"some_file.py": "some content", "some_file_2.py": "some content 2"}
    ]
)
@pytest.mark.asyncio
async def test_additional_files_placed(
    additional_files: dict[str, str]
):
    interactor = CheckSolutionInteractor(
        backend_factory=FakeCompilerFactory(
            FakeCompilerWorksOnlyIfFilePresent,
            expected_files=additional_files
        ),
        fs=FakeFileSystem(),
        sandbox_factory=FakeSandboxFactory()
    )
    result = await interactor(
        test_suite=create_suite(additional_files=additional_files),
        backend_name="doesn't matter now",
        solution=FakeEmptySolution()
    )
    assert result.is_successful


@pytest.mark.parametrize(
    "per_test_files",
    [
        {},
        {"some_file.py": "some content"},
        {"some_file.py": "some content", "some_file_2.py": "some content 2"}
    ]
)
@pytest.mark.asyncio
async def test_per_test_files_placed(
    per_test_files: dict[str, str]
):
    suite = create_suite(
        create_group(
            "A",
            create_test(
                input_files=per_test_files,
                output_files=list(per_test_files.keys())
            )
        )
    )
    interactor = CheckSolutionInteractor(
        backend_factory=FakeCompilerFactory(
            FakeCompilerWorksOnlyIfFilePresentInRuntime,
            expected_files=per_test_files
        ),
        fs=FakeFileSystem(),
        sandbox_factory=FakeSandboxFactory()
    )
    result = await interactor(
        test_suite=suite,
        backend_name="doesn't matter now",
        solution=FakeEmptySolution()
    )
    assert result.is_successful
