from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from apps.kudos.views import update_kudos
from apps.garage.models import Profile

from .forms import TrophiesForm


@login_required
def trophies_edit(request):
    profile = Profile.objects.filter(user=request.user).first()
    form = TrophiesForm(request.POST or None, instance = profile)

    if form.is_valid():
        form.save()
        messages.success(request, "You have updated The Trophies Page")
        return HttpResponseRedirect(request.path_info)

    context ={
        "profile_id": profile.id,
        "form": form,
    }

    return render(request, "trophies/trophies_edit.html", context)
