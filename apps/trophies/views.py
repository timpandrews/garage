from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from apps.kudos.views import update_kudos
from apps.garage.models import Profile

from .forms import TrophiesForm


@login_required
def trophies_view(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user = user)
    trophies = profile.trophies

    context = {
        "trophies": trophies
    }

    return render(request, "trophies/trophies_view.html", context)


@login_required
def trophies_edit(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user = user)
    form = TrophiesForm(instance = user_profile)

    if request.method == "POST":
        form = TrophiesForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "You have updated The Trophies Page")
            return HttpResponseRedirect(request.path_info)

    context ={
        "form": form,
    }

    return render(request, "trophies/trophies_edit.html", context)

