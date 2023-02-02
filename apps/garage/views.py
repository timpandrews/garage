from django.http import HttpResponse
from django.shortcuts import render

def landing(request):
    return render(request, 'garage/landing.html', {})


def add_ride(request):
    return render(request, 'garage/add_new.html', {})
