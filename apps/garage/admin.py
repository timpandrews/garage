from django.contrib import admin
from .models import Doc

class DocAdmin(admin.ModelAdmin):
    fields = ("title", "data")
    list_display = ("id", "title", "data")
    list_display_links = ("id", "title")

admin.site.register(Doc, DocAdmin)
