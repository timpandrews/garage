from django.urls import path

from .views import TrophiesRaw, trophies_fw

# app_name = 'trophies'

urlpatterns = [
    path("trophies/<int:pk>/", TrophiesRaw.as_view(), name="trophies"),
    path("trophies/", trophies_fw, name="trophies_fw"),
]