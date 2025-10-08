from typing import Final

from django.urls import path

from api.views.ping import PingView
from api.views.profiles import (
    GetAllUsersView,
    GetUserByNameView,
    ProfileView,
    SetProfilePictureView,
)
from api.views.register_login import LoginView, RegisterView

urlpatterns: Final = [
    path(
        "api/v1/accounts/ping/",
        PingView.as_view(),
    ),
    path(
        "api/v1/accounts/register/",
        RegisterView.as_view(),
    ),
    path(
        "api/v1/accounts/login/",
        LoginView.as_view(),
    ),
    path(
        "api/v1/accounts/profile/",
        ProfileView.as_view(),
    ),
    path(
        "api/v1/accounts/profile/pic/",
        SetProfilePictureView.as_view(),
    ),
    path(
        "api/v1/accounts/authorize/",
        ProfileView.as_view(),
    ),
    path(
        "api/v1/accounts/user/<str:username>/",
        GetUserByNameView.as_view(),
    ),
    path(
        "api/v1/accounts/all/",
        GetAllUsersView.as_view(),
    ),
    path(
        "api/v1/accounts/user/<str:username>/",
        GetUserByNameView.as_view(),
    ),
]
