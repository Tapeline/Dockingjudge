"""Application module."""

import asyncio
import logging
import os
import uuid

from judgelet.compilers.abc_compiler import (AbstractCompiler,
                                             register_default_compilers)
from judgelet.data.container import SolutionContainer, ZipSolutionContainer
from judgelet.encoding import try_to_decode
from judgelet.exceptions import CompilerNotFoundException
from judgelet.models import RunAnswer, RunRequest, TestCaseResult
from judgelet.runner import SolutionRunner
from judgelet.testing.precompile.abc_precompile_checker import \
    register_default_precompile_checkers
from judgelet.testing.tests import testgroup
from judgelet.testing.tests.testsuite import TestSuite
from judgelet.testing.validators.abc_validator import \
    register_default_validators


class JudgeletApplication:
    """Application class."""

    def __init__(self):
        """Create application and replace event loop if on Windows"""
        if os.name == "nt":
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
        register_default_compilers()
        register_default_validators()
        register_default_precompile_checkers()

    def _serialize_protocol(
            self,
            protocol: list[testgroup.TestGroupProtocol]
    ) -> list[list[TestCaseResult]]:
        """Serialize testing protocol to pydantic-serializable structure"""
        full_protocol = []
        for group_protocol in protocol:
            full_group_protocol = []
            for case in group_protocol:
                full_group_protocol.append(TestCaseResult(
                    return_code=case[0].return_code,
                    stdout=case[0].stdout,
                    stderr=case[0].stderr,
                    verdict=case[1].message,
                    is_successful=case[1].success
                ))
            full_protocol.append(full_group_protocol)
        return full_protocol

    def _ensure_compiler_exists(self, compiler: str) -> None:
        """Validate compiler name"""
        if compiler not in AbstractCompiler.COMPILERS:
            raise CompilerNotFoundException

    async def _execute_request(  # noqa: WPS210 (too many locals)
            self,
            request: RunRequest
    ) -> RunAnswer:
        """Carry out received request"""
        requested_compiler = self._get_requested_compiler(request)
        uid = str(uuid.uuid4())
        place_before = None
        if request.suite.place_files is not None:
            place_before = ZipSolutionContainer.from_b64(request.suite.place_files, "")
        solution_json = request.code
        solution_json["name"] = f"main.{requested_compiler.file_ext}"
        solution = SolutionContainer.from_json(solution_json)
        test_suite = TestSuite.deserialize(request.suite)
        runner = SolutionRunner(uid, place_before, solution, request.compiler, test_suite)
        result = await runner.run()  # noqa: WPS110 (bad name)
        return RunAnswer(
            score=result.score,
            protocol=self._serialize_protocol(result.protocol),
            verdict=result.verdict,
            group_scores=result.group_scores,
            compilation_error=try_to_decode(result.compilation_error)
        )

    def _get_requested_compiler(self, request):
        """Validate compiler name and get the compiler"""
        self._ensure_compiler_exists(request.compiler)
        return AbstractCompiler.COMPILERS[request.compiler]

    async def execute_request_and_handle_errors(self, request: RunRequest):
        """Exactly as the method name says"""
        try:
            return await self._execute_request(request)
        except Exception as exception:
            logging.exception(exception)
            return RunAnswer(
                score=0,
                protocol=[],
                verdict="TSF",
                group_scores={}
            )
