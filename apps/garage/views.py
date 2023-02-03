import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Doc
from .forms import AddNewRide

def landing(response):
    return render(response, 'garage/landing.html', {})


def add_ride(response):
    if response.method == "POST":
        form = AddNewRide(response.POST)
        if form.is_valid():
            print(form.cleaned_data)
            title = form.cleaned_data["title"]
            extra = form.cleaned_data["extra_field"]

            data = {}
            data["extra"] = extra
            print(data)
            
            ride = Doc(title=title, data=data)
            ride.save()

            return HttpResponseRedirect("/")

    else:
        form = AddNewRide()
        context = {
            "form":form,
        }
        return render(response, 'garage/add_new.html', context)
