"""
URL configuration for account_service project.

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
    path("api/accounts/ping/", views.PingView.as_view()),
    path("api/accounts/register/", views.RegisterView.as_view()),
    path("api/accounts/login/", views.LoginView.as_view()),
    path("api/accounts/profile/", views.ProfileView.as_view()),
    path("api/accounts/profile/pic/", views.SetProfilePictureView.as_view()),
    path("api/accounts/authorize/", views.ProfileView.as_view()),
    path("api/accounts/user/<str:username>/", views.GetUserByNameView.as_view()),
    path("api/accounts/all/", views.GetAllUsersView.as_view()),
    path("api/accounts/user/<str:username>/", views.GetUserByNameView.as_view()),
]
