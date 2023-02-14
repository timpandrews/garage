from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .helper import (
    get_week_range,
    get_weekly_rides,
    get_weekly_sums,
    get_distance_history,
    convert_ranges_to_str,
)

@login_required
def dashboard(request):
    user = request.user
    week_range = get_week_range()
    weekly_rides = get_weekly_rides(week_range, user)
    weekly_sums = get_weekly_sums(weekly_rides)
    week = {}
    week["start"] = week_range["start"]
    week["end"] = week_range["end"]
    week["rides"] = len(weekly_rides)
    week["distance"] = weekly_sums["distance"]
    week["time"] = weekly_sums["time"]
    week["elevation"] = weekly_sums["elevation"]
    week["calories"] = weekly_sums["calories"]

    week_ranges, distance_history = get_distance_history(user)
    labels = convert_ranges_to_str(week_ranges)
    labels = labels[::-1]
    data = distance_history[::-1]

    context = {
        "week": week,
        "labels": labels,
        "data": data,
    }

    return render(request, "dashboard/dashboard.html", {'context': context})








