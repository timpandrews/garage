from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('habits/manage/', views.ManageHabits.as_view(), name='manage'),
    path('habits/', views.HabitListView.as_view(), name='list'),
    path('habits/create/', views.HabitCreateView.as_view(), name='create'),
    path('habits/<int:pk>/', views.HabitUpdateView.as_view(), name='update'),
    path('habits/<int:pk>/delete/', views.HabitDeleteView.as_view(), name='delete'),
    path('habits/<int:pk>/detail/', views.HabitDetailView.as_view(), name='detail'),
    path('habits/<int:pk>/update/', views.HabitUpdateView.as_view(), name='update'),
]
