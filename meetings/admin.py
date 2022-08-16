from django.contrib import admin
from .models import *

# 人員出席紀錄
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1


class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "date",
        "location",
        "chairman",
        "minutes_taker",
        "is_archived",
    ]

    inlines = [
        AttendanceInline,
    ]

    # 改成橫的顯示
    filter_horizontal = ("participants",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # 更新admin的many to many field
        meeting = form.instance
        meeting.participants.add(meeting.chairman)
        meeting.participants.add(meeting.minutes_taker)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["meeting", "participant", "attend"]


class EditRequestAdmin(admin.ModelAdmin):
    list_display = ["meeting", "participant", "content"]


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["meeting", "content"]


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ["meeting", "topic", "description", "resolution"]


class AppendixAdmin(admin.ModelAdmin):
    list_display = ["meeting", "provider", "file"]


class AdviceAdmin(admin.ModelAdmin):
    list_display = ["meeting", "participant", "advice"]


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(EditRequest, EditRequestAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Appendix, AppendixAdmin)
admin.site.register(Advice, AdviceAdmin)
