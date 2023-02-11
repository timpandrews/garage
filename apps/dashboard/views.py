from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(response):
    return render(response, "dashboard/dashboard.html", {})
