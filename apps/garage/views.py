from datetime import timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Doc
from .forms import AddNewRide


def landing(response):
    return render(response, "garage/landing.html", {})


def add_ride(response):
    if response.method == "POST":
        form = AddNewRide(response.POST)
        if form.is_valid():
            print(form.cleaned_data)
            title = "ride"
            user_id = 1 # placeholder for user table
            data = form.cleaned_data
            data["duration"] = data["duration"].total_seconds()
            ride = Doc(title=title, user_id=user_id, data=data)
            ride.save()

            return HttpResponseRedirect("/")

    else:
        form = AddNewRide()
        context = {
            "form": form,
        }
        return render(response, "garage/add_new.html", context)
