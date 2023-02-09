from django.contrib import admin

from .models import Doc


class DocAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Fieldset', {'fields': ['user', 'data_type', 'data', 'created', 'updated']}),
    ]
    readonly_fields = ('created', 'updated')
    list_display = ("id", "user", "data_type", "data", "created", "updated")
    list_display_links = ("id", "user", "data_type")

admin.site.register(Doc, DocAdmin)
