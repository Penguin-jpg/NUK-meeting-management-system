from django.urls import path, include
from .views import user_create_view, user_list_view

urlpatterns = [
    path("register/", user_create_view, name="register"),
    path("", include("django.contrib.auth.urls"), name="login"),
    path("", user_list_view, name="user-list"),
]
