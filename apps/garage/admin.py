from django.contrib import admin

from .models import Doc


class DocAdmin(admin.ModelAdmin):
    fields = ("user", "data_type", "data")
    list_display = ("id", "user", "data_type", "data")
    list_display_links = ("id", "user", "data_type")

admin.site.register(Doc, DocAdmin)
