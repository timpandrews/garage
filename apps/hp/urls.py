from django.urls import path
from . import views

from .views import *

app_name = 'hp'

urlpatterns = [
    path('hp/', views.HPListView.as_view(), name='list'),
    path('hp/<int:pk>/detail/', views.HPDetailView.as_view(), name='detail'),
    path('hp/create/', views.HPCreateView.as_view(), name='create'),
    path('hp/create/<str:hp_type>/', views.HPCreateView.as_view(), name='create'),
    path('hp/<int:pk>/update/', views.HPUpdateView.as_view(), name='update'),
    path('hp/<int:pk>/update/<str:hp_type>/', views.HPUpdateView.as_view(), name='update'),
    path('hp/<int:pk>/delete/', views.HPDeleteView.as_view(), name='delete'),
]