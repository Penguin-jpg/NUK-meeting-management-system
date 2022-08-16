from django.urls import path
from .views import (
    user_choose_identity_view,
    user_register_view,
    UserLoginView,
    UserLogoutView,
    no_identity_view,
    user_not_found_view,
    UserListView,
    UserDetailView,
    user_update_view,
    edit_profile_view,
    UserDeleteView,
    meeting_records_view,
)

urlpatterns = [
    path("select/", user_choose_identity_view, name="select-identity"),
    path("register/", user_register_view, name="register"),
    path("identity-error/", no_identity_view, name="no-identity"),
    path("user-not-found/", user_not_found_view, name="user-not-found"),
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
    path("<int:pk>/profile/", UserDetailView.as_view(), name="user-profile"),
    path("<int:id>/edit/", user_update_view, name="user-edit"),
    path("<int:id>/profile/edit/", edit_profile_view, name="edit-profile"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("<int:id>/meeting-records/", meeting_records_view, name="meeting-records"),
]
