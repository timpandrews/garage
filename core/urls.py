from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('apps.garage.urls')),
    path('', include('apps.rides.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.kudos.urls')),
]
