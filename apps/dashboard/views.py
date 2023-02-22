import datetime
from datetime import timedelta, timezone

from dateutil import rrule
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from apps.garage.models import Doc

from .forms import DBMonthForm
from .helper import (convert_ranges_to_str, get_color, get_distance_history,
                     get_last_day_of_month, get_week_range, get_weekly_rides,
                     get_weekly_sums)


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


@login_required
def db_month(request):

    if request.method == 'POST':
        form = DBMonthForm(request.POST)
        if form.is_valid():
            start_year = form.cleaned_data["start_year"]
            end_year = form.cleaned_data["end_year"]
            range_override = True
    else:
        form = DBMonthForm(initial={'end_year': datetime.datetime.now().year})
        range_override = False

    colors = ["#827BC5","#7D8B96","#15807C","#332F32","#C8C1BB","#AB4738","#5B5963"]

    earliest_ride = Doc.objects.filter(user=request.user, active=True).earliest()
    start_date = earliest_ride.data_date
    first_date = start_date.replace(day=1)
    last_date = datetime.datetime.now(timezone.utc)
    print("first_date", first_date, type(first_date))
    print("last_date", last_date, type(last_date))

    month_year = []
    milage = []
    bgColor = []

    # get 1st color for columns
    i = 1
    color = get_color(colors, i)

    if range_override:
        first_date = datetime.datetime(start_year, 1, 1)

        current_year = datetime.datetime.now().year
        if current_year == end_year:
            current_month = datetime.datetime.now().month
            current_month_end_day = get_last_day_of_month(datetime.datetime.now())
            last_date = datetime.datetime(end_year, current_month, current_month_end_day)
        else:
            last_date = datetime.datetime(end_year, 12, 31)


    for dt in rrule.rrule(rrule.MONTHLY, dtstart=first_date, until=last_date):
        year = str(dt.strftime('%Y'))
        month = str(dt.strftime('%m'))
        month_year_str = str(dt.strftime('%b %Y'))
        month_year.append(month_year_str)

        # get new color for columns for each new year
        if month == "01":
            i += 1
            color = get_color(colors, i)
        bgColor.append(color)

        # get monthly milage
        miles_this_year = 0
        rides = Doc.objects.filter(
            user=request.user,
            data_date__year=year,
            data_date__month=month,
            active=True)
        for ride in rides:
            miles_this_year += ride.data["distance"]
        milage.append(round(miles_this_year))

    context = {
        "form": form,
        "labels": month_year,
        "data": milage,
        "bgColor": bgColor,
        "chart_title": "Distance (KM) by Month",
    }

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
