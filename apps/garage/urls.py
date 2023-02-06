from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add_ride, name='add_ride'),
    path('latest', views.latest, name='latest'),
]