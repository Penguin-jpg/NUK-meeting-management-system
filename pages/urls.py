from django.urls import path
from .views import home_view, user_setting

urlpatterns = [
    path("", home_view, name="home"),
    path("setting", user_setting, name="setting"),
]
