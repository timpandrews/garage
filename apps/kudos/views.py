from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.garage.helper import *
from apps.garage.models import Kudos


@login_required
def kudos(request):
    update_kudos(request.user)
    date_ranges = get_date_ranges(date.today(), request.user)

    weekly_kudos = get_weekly_kudos(
        request.user, date_ranges["week_start"], date_ranges["week_end"])

    kudos_rtbp = get_kudos_rtbp(request.user)

    context = {
        "weekly_kudos": weekly_kudos,
        "kudos_rtbp": kudos_rtbp,
    }

    return render(request, "kudos/kudos.html", {'context': context})


@login_required
def trophies(request):
    update_kudos(request.user)
    context = {}

    return render(request, "kudos/trophies.html", {'context': context})


def get_weekly_kudos(user, start, end):
    rides = get_rides_in_range(user, start, end)
    num_rides = len(rides)
    # 1 ride_kudos for each ride
    ride_kudos = num_rides
    # +1 ride_kudos if you ride 3 or more rides per week
    if num_rides >= 3:
        ride_kudos = ride_kudos + 1
    # +2 additional ride_kudos if you ride 5 or more rides per week
    if num_rides >= 5:
        ride_kudos = ride_kudos + 2

    # generate actual kudos
    ride_kudos_list = []
    for kudo in range(ride_kudos):
        ride_kudos_list.append("kudo")

    weekly_kudos = {}
    weekly_kudos["ride_kudos_num"] = ride_kudos
    weekly_kudos["ride_kudos_list"] = ride_kudos_list
    weekly_kudos["user"] = user
    weekly_kudos["start"] = start
    weekly_kudos["end"] = end

    return weekly_kudos


def get_kudos_rtbp(user):
    """
    Get Kudos Ready To Be Places (rtbp)
    """
    kudos = Kudos.objects.filter(user = user, active = True, placed = False)

    return kudos


def update_kudos(user, date_limit="2023-02-13"):
    print("update kudos")

    return None