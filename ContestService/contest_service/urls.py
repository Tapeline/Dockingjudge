from django.urls import path

from api.views.contests import (
    ApplyForContestView,
    CanIManageContestView,
    GetAvailableCompilersView,
    GetContestParticipants,
    GetTimeLeft,
    ListCreateContestView,
    RetrieveUpdateDestroyContestView,
)
from api.views.internal import (
    InternalGetAllTasksView,
    InternalRetrieveCodeTaskView,
    InternalRetrieveQuizTaskView,
)
from api.views.tasks import (
    CanSubmitSolutionToTask,
    ListCreateCodeTaskView,
    ListCreateQuizTaskView,
    ListCreateTextPageView,
    RetrieveUpdateDestroyCodeTaskView,
    RetrieveUpdateDestroyQuizTaskView,
    RetrieveUpdateDestroyTextPageView,
)

urlpatterns = [
    path(
        "api/v1/contests/",
        ListCreateContestView.as_view(),
    ),
    path(
        "api/v1/contests/<int:pk>/",
        RetrieveUpdateDestroyContestView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/tasks/text/",
        ListCreateTextPageView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/tasks/text/<int:pk>/",
        RetrieveUpdateDestroyTextPageView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/tasks/quiz/",
        ListCreateQuizTaskView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/tasks/quiz/<int:pk>/",
        RetrieveUpdateDestroyQuizTaskView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/tasks/code/",
        ListCreateCodeTaskView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/tasks/code/<int:pk>/",
        RetrieveUpdateDestroyCodeTaskView.as_view(),
    ),
    path(
        "api/v1/contests/tasks/<str:task_type>/<int:task_id>/can-submit/<int:user_id>/",
        CanSubmitSolutionToTask.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/time-left/",
        GetTimeLeft.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/apply/",
        ApplyForContestView.as_view(),
    ),
    path(
        "api/v1/contests/compilers/",
        GetAvailableCompilersView.as_view(),
    ),
    path(
        "api/v1/contests/<int:pk>/can-manage/",
        CanIManageContestView.as_view(),
    ),
    path(
        "api/v1/contests/<int:contest_id>/participants/",
        GetContestParticipants.as_view(),
    ),

    path(
        "internal/contests/tasks/quiz/<int:pk>/",
        InternalRetrieveQuizTaskView.as_view(),
    ),
    path(
        "internal/contests/tasks/code/<int:pk>/",
        InternalRetrieveCodeTaskView.as_view(),
    ),
    path(
        "internal/contests/<int:contest_id>/tasks/",
        InternalGetAllTasksView.as_view(),
    ),

]
