from dishka import Provider, provide_all, Scope

from solution_service.application.interactors.get_solution import (
    GetBestSolutionForUserOnTask, GetSolution,
)
from solution_service.application.interactors.list_solutions import (
    ListMySolutions, ListMySolutionsOnTask,
)
from solution_service.application.interactors.post_code_solution import \
    PostCodeSolution
from solution_service.application.interactors.post_quiz_solution import \
    PostQuizSolution
from solution_service.application.interactors.standings import GetStandings
from solution_service.application.interactors.update_solution import \
    StoreCheckedSolution


class InteractorProvider(Provider):
    interactors = provide_all(
        GetBestSolutionForUserOnTask,
        GetSolution,
        GetStandings,
        ListMySolutions,
        ListMySolutionsOnTask,
        PostCodeSolution,
        PostQuizSolution,
        StoreCheckedSolution,
        scope=Scope.REQUEST
    )
