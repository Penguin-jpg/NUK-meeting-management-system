from django.urls import path, include
from django.contrib.auth import authenticate, views
from .views import UserRegisterView, UserListView
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
]
