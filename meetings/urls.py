from django.urls import path
from .views import (
    MeetingListView,
    meeting_create_view,
    edit_meeting_view,
    meeting_delete_view,
    meeting_today_view,
    meeting_not_found_view,
    meeting_participants_view,
    edit_attendance_view,
    edit_request_view,
    request_list_view,
    meeting_not_begin_view,
    announcement_create_view,
    discussion_create_view,
    meeting_detail_view,
    edit_extempore_motion_view,
    edit_announcement_view,
    edit_discussion_view,
    edit_appendix_view,
    send_resolution_view,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting-list"),
    path("create/", meeting_create_view, name="meeting-create"),
    path("meeting-error/", meeting_not_found_view, name="meeting-not-found"),
    path("<int:id>/", meeting_detail_view, name="meeting-detail"),
    path("<int:id>/edit/", edit_meeting_view, name="edit-meeting"),
    path("<int:id>/delete/", meeting_delete_view, name="meeting-delete"),
    path(
        "<int:id>/edit/extemporeMotion",
        edit_extempore_motion_view,
        name="edit-extemporeMotion",
    ),
    path(
        "<int:id>/edit/announcement", edit_announcement_view, name="edit-announcement"
    ),
    path("<int:id>/edit/edit-discussion", edit_discussion_view, name="edit-discussion"),
    path("<int:year>/<int:month>/<int:day>/", meeting_today_view, name="meeting-day"),
    path(
        "<int:id>/participants/", meeting_participants_view, name="meeting-participants"
    ),
    path("<int:id>/edit/attendance/", edit_attendance_view, name="edit-attendance"),
    path("<int:id>/edit/request/", edit_request_view, name="edit-request"),
    path("<int:id>/request-list/", request_list_view, name="request-list"),
    path("meeting-not-begin/", meeting_not_begin_view, name="meeting-not-begin"),
    path(
        "<int:id>/create/announcement",
        announcement_create_view,
        name="announcement-create",
    ),
    path(
        "<int:id>/create/discussion", discussion_create_view, name="discussion-create"
    ),
    path("<int:id>/edit/edit-appendix", edit_appendix_view, name="edit-appendix"),
    path("<int:id>/send-resolution", send_resolution_view, name="send-resolution"),
]
