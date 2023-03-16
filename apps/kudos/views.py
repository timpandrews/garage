from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.garage.helper import *
from apps.garage.models import Doc, Kudos


@login_required
def kudos(request):
    update_kudos(request.user)
    date_ranges = get_date_ranges(date.today(), request.user)

    weekly_kudos = get_weekly_kudos(
        request.user, date_ranges["week_start"], date_ranges["week_end"]
    )

    kudos_rtbp = get_kudos_rtbp(request.user)

    context = {
        "weekly_kudos": weekly_kudos,
        "kudos_rtbp": kudos_rtbp,
    }

    return render(request, "kudos/kudos.html", {"context": context})


def get_weekly_kudos(user, start, end):
    rides = get_rides_in_range(user, start, end)
    num_rides = len(rides)
    # NOTE: 1 ride_kudos for each ride
    ride_kudos = num_rides
    # NOTE:  +1 ride_kudos if you ride 3 or more rides per week
    if num_rides >= 3:
        ride_kudos = ride_kudos + 1
    # NOTE: +2 additional ride_kudos if you ride 5 or more rides per week
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
    Get Kudos Ready To Be Placed (rtbp)
    """
    kudos = Kudos.objects.filter(
        user=user, active=True, placed=False).order_by("created").values()

    return kudos


def update_kudos(user):
    this_week_start = get_date_ranges(date.today(), user)["week_start"]
    # el_act = eligible activities (rides, hps, etc. from DOC model)
    # TODO add other types of activities
    el_act = Doc.objects.filter(
        user=user, doc_type="ride", kudosed=False, doc_date__lt=this_week_start
        ).order_by("doc_date")

    if not el_act: # empty
        eligible_activities = False
    else: # at least one eligible activitie
        eligible_activities = True
        first_act_date = el_act[0].doc_date
        # get date range for first week group of eligable activities
        week_start = get_date_ranges(first_act_date, user)["week_start"].replace(hour=0, minute=0, second=0)
        week_end = get_date_ranges(first_act_date, user)["week_end"].replace(hour=23, minute=59, second=59)

    while eligible_activities:
        # Rides
        # get rides from the each week group
        week_rides = Doc.objects.filter(
            user=user,
            doc_type="ride",
            kudosed=False,
            doc_date__range=(week_start, week_end)
            ).order_by("doc_date")
        print("len week rides:", len(week_rides))

        for act in week_rides:
            # add kudo for each ride
            kudos_data = {
                "ride_id": act.id,
                "desc": "simple ride kudos",
                "type": "ride"
            }
            Kudos.objects.create(
                user=user,
                data=kudos_data,
                type="Rides")

            # one ride has been evaluated marked it as "kudosed"
            Doc.objects.filter(id=act.id).update(kudosed=True)

        # give one extra kudos for weeks with 3+ rides
        if len(week_rides) >= 3:
            kudos_data = {
                "desc": "extra ride kudos for 3+ rides",
                "type": "rides_bonus"
            }
            Kudos.objects.create(
                user=user,
                data=kudos_data,
                type="Rides")

        # give two extra kudos for weeks with 5+ rides
        if len(week_rides) >= 5:
            kudos_data = {
                "desc": "extra ride kudos for 5+ rides",
                "type": "rides_bonus"
            }
            for x in range(2):
                Kudos.objects.create(
                    user=user,
                    data=kudos_data,
                    type="Rides")

        # find any remaing eligable activities
        print("find any remaing eligable activities")
        el_act = Doc.objects.filter(
            user=user, doc_type="ride", kudosed=False, doc_date__lt=this_week_start
            ).order_by("doc_date")
        print("this week start:", this_week_start)
        print(len(el_act))

        if not el_act: # empty
            eligible_activities = False
        else: # at least one eligible activitie
            eligible_activities = True
            first_act_date = el_act[0].doc_date
            # get date range for next week group of eligable activities
            week_start = get_date_ranges(first_act_date, user)["week_start"].replace(hour=0, minute=0, second=0)
            week_end = get_date_ranges(first_act_date, user)["week_end"].replace(hour=23, minute=59, second=59)

