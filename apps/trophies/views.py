import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from apps.garage.models import Profile

from .forms import TrophiesForm


class TrophiesRedirectView(RedirectView):
    print("TrophiesRedirectView")
    def get_redirect_url(self, *args, **kwargs):
        user_id = self.request.user.id
        url = f'/trophies/edit/{user_id}'
        return url



@login_required
def trophies_view(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user = user)
    trophies_edit = profile.trophies_edit
    trophies_view = profile.trophies_view

    context = {
        "trophies_edit": trophies_edit,
        "trophies_view": trophies_view
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
            sub_for_codes(user_profile.id)
            messages.success(request, "You have updated The Trophies Page")
            return HttpResponseRedirect(request.path_info)

    context ={
        "form": form,
    }

    return render(request, "trophies/trophies_edit.html", context)


def sub_for_codes(profile_id):
    print("***sub_for_codes***")
    
    user_profile = Profile.objects.get(id=profile_id)
    trophies_edit = user_profile.trophies_edit
    match_str = "/&lt;([0-9]{6})&gt;"
    match = re.compile(match_str)
    icon = "<i class='bi bi-trophy'></i>"
    trophies_view = re.sub(match, icon, trophies_edit)
    # trophies_view = trophies_edit.replace(">&lt;000042&gt;", "<i class='bi bi-trophy'></i>")
    print("trophies_edit", trophies_edit)
    print("match", match)
    print("trophies_view", trophies_view)

    # Profile.objects.filter(id=profile_id).update(trophies_view=trophies_view)
