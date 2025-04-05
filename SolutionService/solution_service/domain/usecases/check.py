from solution_service.annotations import MutatedArgument
from solution_service.domain.entities.abstract import (AbstractQuizChecker,
                                                       QuizAnswer,
                                                       QuizSolution, QuizCheckerVerdict)


def _verdict_by_success(is_successful: bool) -> str:
    if is_successful:
        return "OK"
    else:
        return "WA"


class CheckQuizSolution:
    def __init__(self, quiz_checker: AbstractQuizChecker):
        self._checker = quiz_checker

    def __call__(
            self,
            submitted_solution: MutatedArgument[QuizSolution]
    ) -> QuizCheckerVerdict:
        verdict = self._checker.check(submitted_solution.submitted_answer)
        submitted_solution.short_verdict = _verdict_by_success(
            verdict.is_successful
        )
        submitted_solution.score = verdict.score
        return verdict
