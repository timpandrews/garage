from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from apps.kudos.views import update_kudos
from apps.garage.models import Profile

from .forms import TrophiesForm


@login_required
def trophies(request):
    update_kudos(request.user)
    context = {}

    return render(request, "trophies/trophies.html", {"context": context})


@login_required
def trophies_fw(request):
    pk = Profile.objects.filter(user=request.user).first()

    return redirect("trophies", pk=pk.id)

class TrophiesRaw(UpdateView):
    model = Profile
    form_class = TrophiesForm
    success_url = reverse_lazy("trophies_fw")
    template_name = "trophies/trophies.html"