from django.urls import path

from . import views

# app_name = 'trophies'

urlpatterns = [
    path("trophies/", views.trophies, name="trophies"),
]