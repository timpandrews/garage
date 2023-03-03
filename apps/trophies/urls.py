from django.urls import path

from .views import trophies_edit, trophies_view

# app_name = 'trophies'

urlpatterns = [
    path("trophies/edit/", trophies_edit, name="trophies_edit"),
    path("trophies/view/", trophies_view, name="trophies_view"),
]