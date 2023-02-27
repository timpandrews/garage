from django.urls import path

from . import views

# app_name = 'kudos'

urlpatterns = [
    path("kudos/", views.kudos, name="kudos"),
    path("trophies/", views.trophies, name="trophies"),
]