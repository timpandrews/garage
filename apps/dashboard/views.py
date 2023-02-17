import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic.base import TemplateView

from apps.garage.models import Doc

from .helper import (convert_ranges_to_str, get_color, get_distance_history,
                     get_week_range, get_weekly_rides, get_weekly_sums)


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


def db_month(request):

    context = {}

    return render(request, "dashboard/month.html", {'context': context})


class db_year(LoginRequiredMixin, TemplateView):
    colors = ["#827BC5","#7D8B96","#15807C","#332F32","#C8C1BB","#AB4738","#5B5963"]
    template_name = "dashboard/year.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        earliest_ride = Doc.objects.filter(user=self.request.user, active=True).earliest()
        start = int(earliest_ride.data_date.strftime("%Y"))
        current = datetime.date.today().year

        years = []
        milage = []
        bgColor = []

        for i, year in enumerate(range(start, current+1)):
            years.append(year)
            bgColor.append(get_color(self.colors, i))

            # get yearly milage
            miles_this_year = 0
            rides = Doc.objects.filter(
                user=self.request.user,
                data_date__year=year,
                active=True)
            for ride in rides:
                miles_this_year += ride.data["distance"]
            milage.append(round(miles_this_year))

        context["labels"] = years
        context["data"] = milage
        context["bgColor"] = bgColor
        context["chart_title"] = "Distance (KM) by Year"
        return context
