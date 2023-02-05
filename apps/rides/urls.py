from django.urls import path
from . import views

app_name = 'rides'

urlpatterns = [
    path('rides/', views.RideListView.as_view(), name='all'), # TODO can i change name to all_rides?
    path('rides/<int:pk>/detail', views.RideDetailView.as_view(), name='ride_detail'),
    path('rides/create/', views.RideCreateView.as_view(), name='ride_create'),
    path('rides/<int:pk>/update/', views.RideUpdateView.as_view(), name='ride_update'),
    path('rides/<int:pk>/delete/', views.RideDeleteView.as_view(), name='ride_delete'),
]