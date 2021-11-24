from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Participant
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
                    "sex",
                    "identity",
                ),
            },
        ),
        # (
        #     "Advanced options",
        #     {
        #         "classes": ("collapse",),
        #         "fields": (""),
        #     },
        # ),
    )


admin.site.register(Participant, ParticipantAdmin)
