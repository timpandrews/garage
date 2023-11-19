from django.urls import path

from .views import TrophiesRedirectView, trophies_edit, trophies_share, trophies_view

app_name = "trophies"

urlpatterns = [
    path("trophies/", TrophiesRedirectView.as_view(), name="trophies"),
    path("trophies/edit/<int:user_id>/", trophies_edit, name="edit"),
    path("trophies/view/<int:user_id>/", trophies_view, name="view"),
    path("<str:username>/", trophies_share, name="share_root"),
    path("trophies/<str:username>", trophies_share, name="share_trophies"),
]
