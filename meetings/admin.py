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
    ]

    inlines = [
        AttendanceInline,
    ]

    # 改成橫的顯示
    filter_horizontal = ("participants",)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["meeting", "participant"]


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(ExtemporeMotion)
admin.site.register(Announcement)
admin.site.register(Discussion)
admin.site.register(Appendix)
