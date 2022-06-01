from django.urls import path
from .views import (
    MeetingCreateView,
    MeetingListView,
    MeetingDetailView,
    MeetingUpdateView,
    MeetingDeleteView,
    meeting_participants_view,
    ArchivedMeetingListView,
    edit_attendance_view,
    request_list_view,
    edit_request_view,
    edit_announcement_view,
    edit_discussion_view,
    edit_appendix_view,
    send_resolution_view,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting-list"),
    path("create/", MeetingCreateView.as_view(), name="meeting-create"),
    path("<int:pk>/", MeetingDetailView.as_view(), name="meeting-detail"),
    path("<int:pk>/edit/", MeetingUpdateView.as_view(), name="edit-meeting"),
    path("<int:pk>/delete/", MeetingDeleteView.as_view(), name="meeting-delete"),
    path(
        "<int:id>/participants/", meeting_participants_view, name="meeting-participants"
    ),
    path("archived/", ArchivedMeetingListView.as_view(), name="archived-meetings"),
    # path("archived/", archived_meeting_view, name="archived-meetings"),
    path("<int:id>/edit-attendances/", edit_attendance_view, name="edit-attendance"),
    path("<int:id>/requests/", request_list_view, name="request-list"),
    path("<int:id>/edit-requests/", edit_request_view, name="edit-requests"),
    path(
        "<int:id>/edit-announcements/",
        edit_announcement_view,
        name="edit-announcements",
    ),
    path("<int:id>/edit-discussions/", edit_discussion_view, name="edit-discussions"),
    path("<int:id>/edit-appendices/", edit_appendix_view, name="edit-appendices"),
    path("<int:id>/send-resolution/", send_resolution_view, name="send-resolution"),
]
