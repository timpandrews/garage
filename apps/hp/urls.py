from django.urls import path
from . import views

from .views import *

app_name = 'hp'

urlpatterns = [
    path('hp/', views.HPListView.as_view(), name='all'),
    path('hp/<int:pk>/detail/', views.HPDetailView.as_view(), name='hp_detail'),
    path('hp/create/', views.HPCreateView.as_view(), name='hp_create'),
    path('hp/create/<str:hp_type>/', views.HPCreateView.as_view(), name='hp_create'),
    path('hp/<int:pk>/update/', views.HPUpdateView.as_view(), name='hp_update'),
    path('hp/<int:pk>/update/<str:hp_type>/', views.HPUpdateView.as_view(), name='hp_update'),
    path('hp/<int:pk>/delete/', views.HPDeleteView.as_view(), name='hp_delete'),
]