from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Participant, Profile
from .forms import SignUpForm, ParticipantChangeForm


class ParticipantAdmin(UserAdmin):
    model = Participant
    add_form = SignUpForm
    form = ParticipantChangeForm
    list_display = [
        "username",
        "last_name",
        "first_name",
        "email",
        "type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "last_name",
                    "first_name",
                    "email",
                    "phone",
                    "type",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "last_name",
                    "first_name",
                    "password1",
                    "password2",
                    "email",
                    "identity",
                ),
            },
        ),
    )


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Profile)
