from django.urls import path

from .views import trophies_edit

# app_name = 'trophies'

urlpatterns = [
    path("trophies/edit/", trophies_edit, name="trophies_edit"),
    # path("trophies/view/", TrophiesView, name="trophies_view"),
]