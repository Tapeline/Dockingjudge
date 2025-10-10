from django.urls import path

from api import views

urlpatterns = [
    path("api/v1/contests/",
         views.ListCreateContestView.as_view()),
    path("api/v1/contests/<int:pk>/",
         views.RetrieveUpdateDestroyContestView.as_view()),
    path("api/v1/contests/<int:contest_id>/tasks/text/",
         views.ListCreateTextPageView.as_view()),
    path("api/v1/contests/<int:contest_id>/tasks/text/<int:pk>/",
         views.RetrieveUpdateDestroyTextPageView.as_view()),
    path("api/v1/contests/<int:contest_id>/tasks/quiz/",
         views.ListCreateQuizTaskView.as_view()),
    path("api/v1/contests/<int:contest_id>/tasks/quiz/<int:pk>/",
         views.RetrieveUpdateDestroyQuizTaskView.as_view()),
    path("api/v1/contests/<int:contest_id>/tasks/code/",
         views.ListCreateCodeTaskView.as_view()),
    path("api/v1/contests/<int:contest_id>/tasks/code/<int:pk>/",
         views.RetrieveUpdateDestroyCodeTaskView.as_view()),
    path("api/v1/contests/tasks/<str:task_type>/<int:task_id>/can-submit/<int:user_id>/",
         views.CanSubmitSolutionToTask.as_view()),
    path("api/v1/contests/<int:contest_id>/time-left/",
         views.GetTimeLeft.as_view()),
    path("api/v1/contests/<int:contest_id>/apply/",
         views.ApplyForContestView.as_view()),
    path("api/v1/contests/compilers/",
         views.GetAvailableCompilersView.as_view()),
    path("api/v1/contests/<int:pk>/can-manage/",
         views.CanIManageContestView.as_view()),
    path("api/v1/contests/<int:contest_id>/participants/",
         views.GetContestParticipants.as_view()),

    path("internal/contests/tasks/quiz/<int:pk>/",
         views.InternalRetrieveQuizTaskView.as_view()),
    path("internal/contests/tasks/code/<int:pk>/",
         views.InternalRetrieveCodeTaskView.as_view()),
    path("internal/contests/<int:contest_id>/tasks/",
         views.InternalGetAllTasksView.as_view()),

]
