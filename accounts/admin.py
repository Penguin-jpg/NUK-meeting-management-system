from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import SignUpForm


class ParticipantAdmin(UserAdmin):
    model = Participant
    add_form = SignUpForm

    list_display = ["username", "last_name", "first_name", "email", "identity"]

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Profile", {"fields": ("last_name", "first_name", "identity")}),
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
        ("Personal Profile", {"fields": ("last_name", "first_name", "identity")}),
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


class ExpertProfileAdmin(admin.ModelAdmin):
    model = ExpertProfile
    list_display = ["user", "company", "title", "telephone", "address", "bank_account"]


class StudentProfileAdmin(admin.ModelAdmin):
    model = StudentProfile
    list_display = ["user", "student_id", "school_system", "grade"]


class TeacherProfileAdmin(admin.ModelAdmin):
    model = TeacherProfile
    list_display = [
        "user",
        "school",
        "department",
        "title",
        "telephone",
        "address",
        "bank_account",
    ]


class AssistantProfileAdmin(admin.ModelAdmin):
    model = AssistantProfile
    list_display = ["user", "telephone"]


class ProfessorProfileAdmin(admin.ModelAdmin):
    model = ProfessorProfile
    list_display = ["user", "title", "telephone"]


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ExpertProfile, ExpertProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(AssistantProfile, AssistantProfileAdmin)
admin.site.register(ProfessorProfile, ProfessorProfileAdmin)
