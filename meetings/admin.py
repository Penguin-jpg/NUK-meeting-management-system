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
            )
        },
    )


admin.site.register(Meeting, MeetingAdmin)
