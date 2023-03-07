import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from collections import defaultdict

from apps.garage.models import Profile, Kudos

from .forms import TrophiesForm


class TrophiesRedirectView(LoginRequiredMixin, RedirectView):
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
            sub_for_codes(user_profile.id, user)
            messages.success(request, "You have updated The Trophies Page")
            return HttpResponseRedirect(request.path_info)

    context ={
        "form": form,
    }

    return render(request, "trophies/trophies_edit.html", context)


def sub_for_codes(profile_id, user):
    print("***sub_for_codes***")

    user_profile = Profile.objects.get(id=profile_id)
    trophies_edit = user_profile.trophies_edit

    # find all codes in trophies_edit
    match_all_code = r"&lt;([A-Fa-f0-9]{6})&gt;"
    codes = re.findall(match_all_code, trophies_edit)
    codes = remove_duplicate_codes(codes)

    # if no matches just replace torphies_view with trophies_edit
    if len(codes) == 0:
        Profile.objects.filter(id=profile_id).update(trophies_view=trophies_edit)

    else: # if there are matches
        trophies_work = trophies_edit
        for code in codes:
            match = r"&lt;" + code + r"&gt;"
            icon = get_kudos_icon(code, user)
            trophies_work = re.sub(match, icon, trophies_work, 1)
            Profile.objects.filter(id=profile_id).update(trophies_view=trophies_work)

    mark_duplicate_codes(match_all_code, trophies_work, profile_id)
    update_kudos_placed_status(codes, user)


def get_kudos_icon(kudos_hex, user):
    print("get_kudos_icon", kudos_hex)
    if is_kudos_valid(kudos_hex, user):
        kudos_detail = Kudos.objects.get(hex=kudos_hex)

        if kudos_detail.data["type"] == "welcome":
            icon = "<a class='mx-1 text-danger' data-bs-toggle='tooltip' title='Welcome'><i class='bi bi-trophy'></i></a>"

        elif kudos_detail.data["type"] == "ride":
            ride_id = kudos_detail.data["ride_id"]
            icon = f"<a href='/rides/{ride_id}/detail' class='mx-1 text-primary' data-bs-toggle='tooltip' title='Kudos for the Ride'><i class='bi bi-trophy'></i></a>"

        elif kudos_detail.data["type"] == "rides_bonus":
            icon = "<a class='mx-1 text-info' data-bs-toggle='tooltip' title='Bonus Kudos for extra Rides'><i class='bi bi-trophy'></i></a>"

        else:
            icon = "<a class='mx-1 text-secondary'><i class='bi bi-trophy'></i></a>"
    else:
        icon = f"<***invalid code:{kudos_hex}***>"

    return icon


def update_kudos_placed_status(codes, user):
    # Set all kudos for user to unplaced
    Kudos.objects.filter(user=user).update(placed=False)

    # then loop through each used code and marked as placed
    # if no codes user, then all kudos remain unplaced
    for code in codes:
        Kudos.objects.filter(hex=code).update(placed=True)


def is_kudos_valid(kudos_hex, user):
    try:
        valid_kudos = Kudos.objects.get(hex=kudos_hex, user=user)
        valid = True
    except Kudos.DoesNotExist:
        valid = False

    return valid


def remove_duplicate_codes(codes):
    # find dups and create a dictionary with duplicate codes and their
    # indicies
    Dups = defaultdict(list)
    for i,code in enumerate(codes):
        Dups[code].append(i)
    Dups = {k:v for k,v in Dups.items() if len(v)>1}

    # loop through dups & then loop through codes and remove 2nd and
    # subsiquent occurences of dups.
    for dup_code in Dups:
        dups = 0
        for i, code in enumerate(codes):
            if dup_code == code:
                dups += 1
                if dups > 1:
                    del codes[i]

    return codes


def mark_duplicate_codes(match, trophies_work, profile_id):
    dup_codes = re.findall(match, trophies_work)

    if len(dup_codes) > 0:
        for dup_code in dup_codes:
            match = r"&lt;" + dup_code + r"&gt;"
            icon = f"<***duplicate code:{dup_code}***>"
            trophies_work = re.sub(match, icon, trophies_work, 1)
            Profile.objects.filter(id=profile_id).update(trophies_view=trophies_work)