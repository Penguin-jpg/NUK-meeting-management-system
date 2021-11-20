from django.urls import path, include
from .views import UserRegisterView, UserListView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("", include("django.contrib.auth.urls"), name="login"),
    path("", UserListView.as_view(), name="user-list"),
]
