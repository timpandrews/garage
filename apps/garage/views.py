from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Doc


def landing(response):
    return render(response, "garage/landing.html", {})