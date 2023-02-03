from django.contrib import admin
from .models import Doc

class DocAdmin(admin.ModelAdmin):
    fields = ("user_id", "data_type", "data")
    list_display = ("id", "user_id", "data_type", "data")
    list_display_links = ("id", "user_id", "data_type")

admin.site.register(Doc, DocAdmin)
