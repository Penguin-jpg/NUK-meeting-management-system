from django.urls import path, include
from .views import (
    MeetingListView,
    MeetingCreateView,
    MeetingDetailView,
    edit_meeting_view,
    meeting_today_view,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting-list"),
    path("create/", MeetingCreateView.as_view(), name="meeting-create"),
    path("<int:id>/", MeetingDetailView.as_view(), name="meeting-detail"),
    path("edit/<int:id>/", edit_meeting_view, name="edit-meeting"),
    path("<int:year>/<int:month>/<int:day>/", meeting_today_view, name="meeting-day"),
]
