from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('add', views.add_ride, name='add_ride')
]