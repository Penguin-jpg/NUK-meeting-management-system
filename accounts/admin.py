from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import ParticipantChangeForm, SignUpForm


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


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ExpertInfo)
admin.site.register(StudentInfo)
admin.site.register(TeacherInfo)
admin.site.register(AssistantInfo)
admin.site.register(ProfessorInfo)
