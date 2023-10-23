from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('habits/', views.Habits.as_view(), name='habits'),
]
