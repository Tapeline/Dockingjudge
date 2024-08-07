"""
URL configuration for contest_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('contests/',
         views.ListCreateContestView.as_view()),
    path('contests/<int:pk>/',
         views.RetrieveUpdateDestroyContestView.as_view()),
    path('contests/<int:contest_id>/tasks/text/',
         views.ListCreateTextPageView.as_view()),
    path('contests/<int:contest_id>/tasks/text/<int:pk>/',
         views.RetrieveUpdateDestroyTextPageView.as_view()),
    path('contests/<int:contest_id>/tasks/quiz/',
         views.ListCreateQuizTaskView.as_view()),
    path('contests/<int:contest_id>/tasks/quiz/<int:pk>/',
         views.RetrieveUpdateDestroyQuizTaskView.as_view()),
    path('contests/<int:contest_id>/tasks/code/',
         views.ListCreateCodeTaskView.as_view()),
    path('contests/<int:contest_id>/tasks/code/<int:pk>/',
         views.RetrieveUpdateDestroyCodeTaskView.as_view()),
    path('contests/tasks/<str:task_type>/<int:task_id>/can-submit/<int:user_id>/',
         views.CanSubmitSolutionToTask.as_view()),
    path('contests/<int:contest_id>/time-left/',
         views.GetTimeLeft.as_view()),

    path('contests/internal/tasks/quiz/<int:pk>/',
         views.InternalRetrieveQuizTaskView.as_view()),
    path('contests/internal/tasks/code/<int:pk>/',
         views.InternalRetrieveCodeTaskView.as_view()),

]
