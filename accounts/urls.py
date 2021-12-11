from django.urls import path
from .views import (
    user_choose_identity_view,
    user_register_view,
    UserLoginView,
    UserLogoutView,
    no_identity_view,
    user_info_view,
    edit_info_view,
    UserListView,
)
from .forms import LoginForm

urlpatterns = [
    path("select/", user_choose_identity_view, name="select-identity"),
    path("register/", user_register_view, name="register"),
    path("idt_error/", no_identity_view, name="no-identity"),
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),
    path(
        "logout",
        UserLogoutView.as_view(),
        name="logout",
    ),
    path("", UserListView.as_view(), name="user-list"),
    path("info/<int:id>/", user_info_view, name="user-info"),
    path("info/edit/<int:id>/", edit_info_view, name="edit-info"),
]
