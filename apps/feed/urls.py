from django.urls import path

from .views import feed as view_feed

app_name = 'feed'

urlpatterns = [
    path("feed/", view_feed, name="feed"),
]