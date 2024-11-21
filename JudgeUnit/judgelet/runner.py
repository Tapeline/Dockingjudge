"""
Provides classes for testing solutions
"""

import os
import shutil

from judgelet.data.container import (SolutionContainer,
                                     ZipSolutionContainer,
                                     place_all_solution_files)
from judgelet.testing.tests.testsuite import TestSuite, SuiteResult


class SolutionRunner:
    """Runs and tests solutions"""
    # pylint: disable=too-many-arguments
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-positional-arguments

    def __init__(self,
                 uid: str,
                 place_before: ZipSolutionContainer | None,
                 solution: SolutionContainer,
                 compiler_name: str,
                 test_suite: TestSuite):
        self._uid = uid
        self._compiler_name = compiler_name
        self._place_before = place_before
        self._solution = solution
        self._working_dir = f"solution/{self._uid}"
        self._suite = test_suite

    def _prepare_solution_environment(self):
        """Create solution directory and place additional files"""
        try:
            os.mkdir("solution")
        except FileExistsError:
            pass
        os.mkdir(self._working_dir)
        if self._place_before is not None:
            place_all_solution_files(self._place_before, self._working_dir)

    def _place_solution_files(self) -> str:
        """Place main solution files and return main file name"""
        place_all_solution_files(self._solution, self._working_dir)
        return self._solution.get_main_file()

    async def _run_suite(self, main_file) -> SuiteResult:
        """Call to TestSuite to run tests"""
        return await self._suite.run_suite(
            self._compiler_name,
            main_file,
            self._working_dir,
            [file.name for file in self._solution.get_files()]
        )

    def _clean_up(self):
        """Delete solution directory"""
        shutil.rmtree(self._working_dir)

    async def run(self) -> SuiteResult:
        """Test solution"""
        self._prepare_solution_environment()
        main_file = self._place_solution_files()
        result = await self._run_suite(main_file)
        self._clean_up()
        return result
