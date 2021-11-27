from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Participant, Profile


class ParticipantAdmin(UserAdmin):
    model = Participant

    list_display = ["username", "last_name", "first_name", "email", "type"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "type")}),
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
        (None, {"fields": ("username", "password1", "password2")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "type")}),
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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "sex", "phone"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "sex",
                    "phone",
                    "telephone",
                    "title",
                    "address",
                    "bank_account",
                    "company",
                    "school",
                    "department",
                    "student_id",
                    "school_system",
                    "grade",
                )
            },
        ),
    )

    add_fieldsets = (
        None,
        {
            "fields": (
                "user",
                "sex",
                "phone",
                "telephone",
                "title",
                "address",
                "bank_account",
                "company",
                "school",
                "department",
                "student_id",
                "school_system",
                "grade",
            )
        },
    )


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Profile, ProfileAdmin)
