from django.contrib import admin

from .models import Doc, Kudos, Profile, ZwiftRouteList


class DocAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fieldset", {
            "fields": [
                "id",
                "user",
                "doc_type",
                "doc_date",
                "data",
                "fit_data",
                "gpx_data",
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
        "created",
        "updated",
        "active",
    )
    list_display_links = ("id", "user", "doc_type")
    list_editable = ("active", "kudosed",)
    # list_filter = ("user", "doc_type", "kudosed")
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


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "profile_pic",
    )
    list_display_links = ("id", "user")
admin.site.register(Profile, ProfileAdmin)


class ZwiftRouteListAdmin(admin.ModelAdmin):
    list_display = (
        "route_name",
        "world_name",
    )
    list_display_links = ("route_name",)
    ordering = ('world_name', 'route_name',)
admin.site.register(ZwiftRouteList, ZwiftRouteListAdmin)