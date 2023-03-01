from django.contrib import admin

from .models import Doc, Kudos, UserProfile


class DocAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fieldset", {
            "fields": [
                "id",
                "user",
                "doc_type",
                "doc_date",
                "data",
                "created",
                "updated",
                "active",
                "kudosed",
                ]
            }
        ),
    ]
    readonly_fields = ("id", "created", "updated")
    list_display = (
        "id",
        "user",
        "doc_type",
        "doc_date",
        "kudosed",
        "data",
        "created",
        "updated",
        "active",
    )
    list_display_links = ("id", "user", "doc_type")
    list_editable = ("active", "kudosed",)
    list_filter = ("user", "doc_type", "kudosed")
admin.site.register(Doc, DocAdmin)


class KudosAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fieldset", {
            "fields": [
                "hex",
                "key",
                "user",
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


class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)