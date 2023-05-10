from django.urls import path

from .views import FeedView, DetailView

app_name = 'feed'

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    path("feed/<int:doc_id>/", DetailView.as_view(), name="detail"),
]