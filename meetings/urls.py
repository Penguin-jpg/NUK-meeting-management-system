from django.urls import path, include
from .views import MeetingListView, MeetingDetailView

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting-list"),
    path("<int:id>/", MeetingDetailView.as_view(), name="meeting-detail"),
]
