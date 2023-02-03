from django.contrib import admin
from .models import Doc

class DocAdmin(admin.ModelAdmin):
    fields = ("title", "user_id", "data")
    list_display = ("id", "title", "user_id", "data")
    list_display_links = ("id", "title")

admin.site.register(Doc, DocAdmin)
