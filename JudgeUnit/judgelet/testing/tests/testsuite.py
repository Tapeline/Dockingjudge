from judgelet.compilers.abc_compiler import RunResult
from judgelet.testing.tests.testgroup import TestGroup
from judgelet.testing.validators.abc_validator import ValidatorAnswer
from judgelet import models


class TestSuite:
    groups: list[TestGroup]
    group_dependencies: dict[str, set[str]]

    def __init__(self, groups: list[TestGroup], group_dependencies: dict[str, set[str]]):
        self.groups = groups
        self.group_dependencies = group_dependencies

    async def run_suite(self, compiler_name: str, file_name: str) \
            -> tuple[int, list[list[tuple[RunResult, ValidatorAnswer]]], dict, str]:
        score = 0
        fully_passed = set()
        full_protocol = []
        group_scores = {}
        verdict = None
        for group in self.groups:
            has_passed, group_score, group_protocol, group_verdict = \
                await group.get_result(compiler_name, file_name)
            full_protocol.append(group_protocol)
            if group.name not in self.group_dependencies:
                fully_passed.add(group.name)
                score += group_score
                group_scores[group.name] = group_score
            elif all(dep in fully_passed for dep in self.group_dependencies[group.name]):
                fully_passed.add(group.name)
                score += group_score
                group_scores[group.name] = group_score
            if not has_passed and verdict is None:
                verdict = group_verdict
        return score, full_protocol, group_scores, verdict or "OK"

    @staticmethod
    def deserialize(groups: list[models.TestGroup]) -> "TestSuite":
        groups = [TestGroup.deserialize(group)
                  for group in groups]
        deps = {group.name: set() for group in groups}
        for group in groups:
            for dep in group.depends_on:
                deps[group.name].add(dep)

        return TestSuite(groups, deps)
