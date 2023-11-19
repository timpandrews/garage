from django.urls import path

from .views import dashboard, db_month, db_year, dbnew

app_name = "dashboard"

urlpatterns = [
    path("dashboard/", dashboard, name="db"),
    path("db2", dbnew.as_view(), name="db2"),
    path("dashboard/month/", db_month, name="db_month"),
    path("dashboard/year/", db_year.as_view(), name="db_year"),
]
