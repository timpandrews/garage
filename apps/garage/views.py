from django.http import HttpResponse
from django.shortcuts import render

def landing(request):
    return HttpResponse("<h1>Cyclists Garage</h1>")
