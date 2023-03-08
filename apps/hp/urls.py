from django.urls import path
from . import views

# app_name = 'hp'

urlpatterns = [
    path("hp/", views.hp, name="hp"),
]