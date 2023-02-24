from django.contrib import admin

from .models import Doc, Kudos


class DocAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fieldset", {
            "fields": [
                "id",
                "user",
                "data_type",
                "data_date",
                "data",
                "created",
                "updated",
                "active"
                ]
            }
        ),
    ]
    readonly_fields = ("created", "updated")
    list_display = (
        "id",
        "user",
        "data_type",
        "data_date",
        "data",
        "created",
        "updated",
        "active",
    )
    list_display_links = ("id", "user", "data_type")
admin.site.register(Doc, DocAdmin)


class KudosAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fieldset", {
            "fields": [
                "user",
                "key",
                "type",
                "data",
                "created",
                "updated",
                "active",
                "placed",
                ]
            }
        ),
    ]
    readonly_fields = ("created", "updated")
    list_display = (
        "id",
        "key",
        "user",
        "type",
        "data",
        "created",
        "updated",
        "active",
        "placed",
    )
    list_display_links = ("id", "key")

admin.site.register(Kudos, KudosAdmin)