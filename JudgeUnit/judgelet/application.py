"""
Application module
"""

import asyncio
import logging
import os
import uuid

from judgelet.compilers.abc_compiler import (Compiler, RunResult,
                                             register_default_compilers)
from judgelet.data.container import ZipSolutionContainer, SolutionContainer
from judgelet.exceptions import CompilerNotFoundException
from judgelet.models import TestCaseResult, RunRequest, RunAnswer
from judgelet.runner import SolutionRunner
from judgelet.testing.precompile.abc_precompile_checker import (
    register_default_precompile_checkers)
from judgelet.testing.tests.testsuite import TestSuite
from judgelet.testing.validators.abc_validator import (
    ValidatorAnswer, register_default_validators)


class JudgeletApplication:
    """Application class"""
    def __init__(self):
        if os.name == "nt":
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
        register_default_compilers()
        register_default_validators()
        register_default_precompile_checkers()

    def serialize_protocol(
            self, protocol: list[list[tuple[RunResult, ValidatorAnswer]]]
    ) -> list[list[TestCaseResult]]:
        """Serializes testing protocol to pydantic-serializable structure"""
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

    def ensure_compiler_exists(self, compiler) -> None:
        """Compiler validation"""
        if compiler not in Compiler.COMPILERS:
            raise CompilerNotFoundException

    async def execute_request(self, request: RunRequest) -> RunAnswer:
        # pylint: disable=missing-function-docstring
        self.ensure_compiler_exists(request.compiler)
        uid = str(uuid.uuid4())
        place_before = None
        if request.suite.place_files is not None:
            place_before = ZipSolutionContainer.from_b64(request.suite.place_files, "")
        solution_json = request.code
        solution_json["name"] = f"main.{Compiler.COMPILERS[request.compiler].file_ext}"
        solution = SolutionContainer.from_json(solution_json)
        test_suite = TestSuite.deserialize(request.suite)
        runner = SolutionRunner(uid, place_before, solution, request.compiler, test_suite)
        score, protocol, group_scores, verdict = await runner.run()
        converted_protocol = self.serialize_protocol(protocol)
        return RunAnswer(
            score=score,
            protocol=converted_protocol,
            verdict=verdict,
            group_scores=group_scores
        )

    async def execute_request_and_handle_errors(self, request: RunRequest):
        # pylint: disable=missing-function-docstring
        # pylint: disable=broad-exception-caught
        try:
            return await self.execute_request(request)
        except Exception as e:
            logging.exception(e)
            return RunAnswer(
                score=0,
                protocol=[],
                verdict="TSF",
                group_scores={}
            )
