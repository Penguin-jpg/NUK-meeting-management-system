from django.urls import path
from .views import (
    MeetingListView,
    meeting_create_view,
    # MeetingDetailView,
    edit_meeting_view,
    meeting_delete_view,
    meeting_today_view,
    meeting_not_found_view,
    meeting_participants_view,
    edit_attendance_view,
    meeting_not_begin_view,
    extemporeMotion_create_view,
    announcement_create_view,
    discussion_create_view,
    meeting_detail_view,
    edit_extempore_motion_view,
    edit_announcement_view,
    edit_discussion_view,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting-list"),
    path("create/", meeting_create_view, name="meeting-create"),
    path("meeting_error/", meeting_not_found_view, name="meeting-not-found"),
    path("<int:id>/", meeting_detail_view, name="meeting-detail"),
    # path("<int:id>/", MeetingDetailView.as_view(), name="meeting-detail"),
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
    path("meeting_not_begin/", meeting_not_begin_view, name="meeting-not-begin"),
    path(
        "<int:id>/create/extemporeMotion",
        extemporeMotion_create_view,
        name="extemporeMotion-create",
    ),
    path(
        "<int:id>/create/announcement",
        announcement_create_view,
        name="announcement-create",
    ),
    path(
        "<int:id>/create/discussion", discussion_create_view, name="discussion-create"
    ),
]
