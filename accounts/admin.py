from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import ParticipantChangeForm, SignUpForm
from meetings.models import Meeting

# 出席過的會議
class MeetingRecordInline(admin.TabularInline):
    model = Meeting.attendance_record.through
    extra = 1


class ParticipantAdmin(UserAdmin):
    model = Participant
    form = ParticipantChangeForm
    add_form = SignUpForm

    list_display = ["username", "last_name", "first_name", "email", "identity"]

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("last_name", "first_name", "identity")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"fields": ("username", "email", "password1", "password2")}),
        ("Personal info", {"fields": ("last_name", "first_name", "identity")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    inlines = [
        MeetingRecordInline,
    ]


class ExpertInfoAdmin(admin.ModelAdmin):
    model = ExpertInfo
    list_display = ["user", "company", "title", "telephone", "address", "bank_account"]


class StudentInfoAdmin(admin.ModelAdmin):
    model = StudentInfo
    list_display = ["user", "student_id", "school_system", "grade"]


class TeacherInfoAdmin(admin.ModelAdmin):
    model = TeacherInfo
    list_display = [
        "user",
        "school",
        "department",
        "title",
        "telephone",
        "address",
        "bank_account",
    ]


class AssistantInfoAdmin(admin.ModelAdmin):
    model = AssistantInfo
    list_display = ["user", "telephone"]


class ProfessorInfoAdmin(admin.ModelAdmin):
    model = ProfessorInfo
    list_display = ["user", "title", "telephone"]


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ExpertInfo, ExpertInfoAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.register(TeacherInfo, TeacherInfoAdmin)
admin.site.register(AssistantInfo, AssistantInfoAdmin)
admin.site.register(ProfessorInfo, ProfessorInfoAdmin)
