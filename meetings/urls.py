from django.urls import path, include
from .views import meeting_list_view, meeting_detail_view

urlpatterns = [
    path("", meeting_list_view, name="meeting-list"),
    path("<int:id>/", meeting_detail_view, name="meeting-detail"),
]
