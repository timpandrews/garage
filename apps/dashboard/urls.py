from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path("dashboard/", views.dashboard, name="db"),
    path("dashboard/month/", views.db_month, name="db_month"),
    path("dashboard/year/", views.db_year.as_view(), name="db_year"),
]