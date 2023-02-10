from django.shortcuts import render

def dashboard(response):
    return render(response, "dashboard/dashboard.html", {})
