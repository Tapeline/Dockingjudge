import asyncio
import os
import shutil
import uuid

from judgelet.compilers.abc_compiler import Compiler, RunResult, register_default_compilers
from judgelet.exceptions import CompilerNotFoundException
from judgelet.models import TestCaseResult, RunRequest, RunAnswer
from judgelet.testing.tests.testsuite import TestSuite
from judgelet.testing.validators.abc_validator import ValidatorAnswer, register_default_validators


class JudgeletApplication:
    def __init__(self):
        if os.name == "nt":
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
        register_default_compilers()
        register_default_validators()

    def shutdown(self):
        shutil.rmtree("solution")

    def prepare_solution_environment(self, uid, code, compiler_extension):
        try:
            os.mkdir("solution")
        except FileExistsError:
            pass
        os.mkdir(f"solution/{uid}")
        with open(f"solution/{uid}/program.{compiler_extension}", "w") as file:
            file.write(code)
        return f"solution/{uid}/program.{compiler_extension}"

    def purge_solution_environment(self, uid):
        shutil.rmtree(f"solution/{uid}")

    def serialize_protocol(self, protocol: list[list[tuple[RunResult, ValidatorAnswer]]]):
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

    def ensure_compiler_exists(self, compiler):
        if compiler not in Compiler.COMPILERS:
            raise CompilerNotFoundException

    async def execute_request(self, request: RunRequest) -> RunAnswer:
        uid = str(uuid.uuid4())
        file_name = self.prepare_solution_environment(
            uid, request.code, Compiler.COMPILERS[request.compiler].file_ext
        )
        test_suite = TestSuite.deserialize(request.suite)
        score, protocol, group_scores, verdict = await test_suite.run_suite(request.compiler, file_name)
        converted_protocol = self.serialize_protocol(protocol)
        return RunAnswer(
            score=score,
            protocol=converted_protocol,
            verdict=verdict,
            group_scores=group_scores
        )
