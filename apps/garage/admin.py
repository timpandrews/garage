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
                "active",
                "kudosed",
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
        "kudosed",
    )
    list_display_links = ("id", "user", "data_type")
admin.site.register(Doc, DocAdmin)


class KudosAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fieldset", {
            "fields": [
                "hex",
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
        "hex",
        "key",
        "user",
        "type",
        "data",
        "created",
        "updated",
        "active",
        "placed",
    )
    list_display_links = ("id", "hex", "key")

admin.site.register(Kudos, KudosAdmin)