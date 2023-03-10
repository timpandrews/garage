from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path("jsil8n", JavaScriptCatalog.as_view(), name="js-catalog"),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('apps.garage.urls')),
    path('', include('apps.rides.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.kudos.urls')),
    path('', include('apps.trophies.urls')),
    path('', include('apps.hp.urls')),
]

handler404 = 'apps.garage.views.error_404_view'
handler500 = 'apps.garage.views.error_500_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
