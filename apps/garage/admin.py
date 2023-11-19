from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import Doc, Kudos, Profile, ZwiftRouteList


class DocResource(resources.ModelResource):
    """
    Resource class for the Doc model.  Used with django-import-export
    library.
    """

    class Meta:
        model = Doc


class DocAdmin(ImportExportActionModelAdmin):
    """
    Admin class for managing Doc objects.

    This class defines the configuration options for the admin interface
    for the Doc model. It specifies the fieldsets, readonly fields,
    list display options, list editable fields, and list filter options.

    It uses the ImportExportActionModelAdmin class from the django-import-export
    library to add import and export functionality to the admin interface.
    """

    resource_classes = [DocResource]

    fieldsets = [
        (
            "Fieldset",
            {
                "fields": [
                    "id",
                    "user",
                    "doc_type",
                    "doc_date",
                    "data",
                    "detail",
                    "fit_data",
                    "gpx_data",
                    "created",
                    "updated",
                    "active",
                    "kudosed",
                ]
            },
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
    list_editable = (
        "active",
        "kudosed",
    )
    list_filter = ("doc_type", "kudosed", "user")


admin.site.register(Doc, DocAdmin)


class KudosAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Fieldset",
            {
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
            },
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
    ordering = (
        "world_name",
        "route_name",
    )


admin.site.register(ZwiftRouteList, ZwiftRouteListAdmin)
