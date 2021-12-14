from django.urls import path
from .views import (
    MeetingListView,
    meeting_create_view,
    MeetingDetailView,
    edit_meeting_view,
    meeting_today_view,
    meeting_not_found_view,
    meeting_participants_view,
    edit_attendance_view,
    meeting_not_begin_view,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting-list"),
    path("create/", meeting_create_view, name="meeting-create"),
    path("meeting_error/", meeting_not_found_view, name="meeting-not-found"),
    path("<int:id>/", MeetingDetailView.as_view(), name="meeting-detail"),
    path("<int:id>/edit/", edit_meeting_view, name="edit-meeting"),
    path("<int:year>/<int:month>/<int:day>/", meeting_today_view, name="meeting-day"),
    path(
        "<int:id>/participants/", meeting_participants_view, name="meeting-participants"
    ),
    path("<int:id>/edit/attendance/", edit_attendance_view, name="edit-attendance"),
    path("meeting_not_begin/", meeting_not_begin_view, name="meeting-not-begin"),
]
