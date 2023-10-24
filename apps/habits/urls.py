from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('habits/manage/', views.Habits.as_view(), name='manage'),
]
