"""
URL configuration for solution_service project.

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
from django.urls import path

from api import views

urlpatterns = [
    path("api/solutions/my/code/",
         views.ListMyCodeSolutionsView.as_view()),
    path("api/solutions/my/quiz/",
         views.ListMyQuizSolutionsView.as_view()),
    path("api/solutions/for-task/code/<int:task_id>/",
         views.ListTaskCodeSolutionsView.as_view()),
    path("api/solutions/for-task/quiz/<int:task_id>/",
         views.ListTaskQuizSolutionsView.as_view()),
    path("api/solutions/post/<str:task_type>/<int:task_id>/",
         views.SubmitSolutionView.as_view()),
    path("api/solutions/get/code/<int:pk>/",
         views.RetrieveCodeSolutionView.as_view()),
    path("api/solutions/get/quiz/<int:pk>/",
         views.RetrieveQuizSolutionView.as_view()),
    path("api/solutions/get-score/",
         views.GetTasksScoreForUserView.as_view()),
]
