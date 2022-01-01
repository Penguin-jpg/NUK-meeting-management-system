from django.urls import path
from .views import (
    user_choose_identity_view,
    user_register_view,
    UserLoginView,
    UserLogoutView,
    no_identity_view,
    user_not_found_view,
    user_info_view,
    edit_info_view,
    UserListView,
    meeting_record_view,
)

urlpatterns = [
    path("select/", user_choose_identity_view, name="select-identity"),
    path("register/", user_register_view, name="register"),
    path("identity-error/", no_identity_view, name="no-identity"),
    path("user-error/", user_not_found_view, name="user-not-found"),
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
    path("<int:id>/info/", user_info_view, name="user-info"),
    path("<int:id>/info/edit/", edit_info_view, name="edit-info"),
    path("<int:id>/meeting-record/", meeting_record_view, name="meeting-record"),
]
