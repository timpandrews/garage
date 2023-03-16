from django.urls import path

from .views import *

app_name = 'rides'

urlpatterns = [
    path('rides/', RideListView.as_view(), name='list'),
    path('rides/<int:pk>/detail/', RideDetailView.as_view(), name='detail'),
    path('rides/create/', RideCreateView.as_view(), name='create'),
    path('rides/<int:pk>/update/', RideUpdateView.as_view(), name='update'),
    path('rides/<int:pk>/delete/', RideDeleteView.as_view(), name='delete'),
    path('rides/import/fit/', ride_import_fit, name='import_fit'),
]