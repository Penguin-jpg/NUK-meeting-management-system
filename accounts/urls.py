from django.urls import path
from django.contrib.auth import views
from .views import (
    UserRegisterView,
    UserListView,
    UserDeleteView,
    user_profile_view,
    edit_profile_view,
)
from .forms import LoginForm

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "login/",
        views.LoginView.as_view(
            template_name="registration/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path(
        "logout",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path("", UserListView.as_view(), name="user-list"),
    path("delete/<int:id>/", UserDeleteView.as_view(), name="user-delete"),
    path(
        "profile/<int:id>",
        user_profile_view,
        name="user-profile",
    ),
    path("profile/edit/<int:id>", edit_profile_view, name="edit-profile"),
]
