from django.contrib import admin
from .models import Meeting


class MeetingAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "date"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "date",
                    "location",
                    "chairman",
                    "minutes_taker",
                    "participants",
                )
            },
        ),
    )

    add_fieldsets = (
        None,
        {
            "fields": (
                "name",
                "type",
                "date",
                "location",
                "chairman",
                "minutes_taker",
                "participants",
            )
        },
    )

    filter_horizontal = ("participants",)


admin.site.register(Meeting, MeetingAdmin)
