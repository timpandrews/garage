from django.urls import path

from .views import trophies_edit, trophies_view, TrophiesRedirectView

# app_name = 'trophies'

urlpatterns = [
    path("trophies/", TrophiesRedirectView.as_view(), name="trophies"),
    path("trophies/edit/<int:user_id>", trophies_edit, name="trophies_edit"),
    path("trophies/view/<int:user_id>", trophies_view, name="trophies_view"),
]
