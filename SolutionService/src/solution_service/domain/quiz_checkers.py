import re
from dataclasses import dataclass

import Levenshtein

from solution_service.domain.abstract import (
    AbstractQuizChecker,
    QuizAnswer,
    QuizCheckerVerdict,
)


@dataclass
class QuizTextCheckerParams:
    pattern: str
    case_insensitive: bool = False
    strict_match: bool = True


class QuizTextChecker(AbstractQuizChecker):
    params: QuizTextCheckerParams
    name = "text"

    def check(
            self,
            actual_answer: QuizAnswer,
    ) -> QuizCheckerVerdict:
        actual_answer = self._apply_case_sensitivity(actual_answer)
        expected_answer = self._apply_case_sensitivity(self.params.pattern)
        score = self._calculate_score(actual_answer, expected_answer)
        is_successful = score == self.max_score
        return QuizCheckerVerdict(
            score=score,
            is_successful=is_successful,
        )

    def _apply_case_sensitivity(self, answer: QuizAnswer) -> QuizAnswer:
        if self.params.case_insensitive:
            return answer.lower()
        return answer

    def _calculate_score(
            self,
            actual_answer: QuizAnswer,
            expected_answer: QuizAnswer,
    ) -> int:
        if not self.params.strict_match:
            dist = Levenshtein.jaro_winkler(actual_answer, expected_answer)
            return int(dist * self.max_score)
        return self.max_score if actual_answer == expected_answer else 0


@dataclass
class QuizTextRegexCheckerParams:
    pattern: str


class QuizTextRegexChecker(AbstractQuizChecker):
    params: QuizTextRegexCheckerParams
    name = "regex"

    def check(
            self,
            actual_answer: QuizAnswer,
    ) -> QuizCheckerVerdict:
        match = re.fullmatch(self.params.pattern, actual_answer)
        had_match = match is not None
        return QuizCheckerVerdict(
            score=self.max_score if had_match else 0,
            is_successful=had_match,
        )
