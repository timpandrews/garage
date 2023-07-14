import datetime
from datetime import timedelta, timezone

import pytz
from dateutil import rrule
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from tzlocal import get_localzone

from apps.garage.models import Doc
from common.tools import convert_to_imperial, get_unit_names

from .forms import DBMonthForm
from .helper import (convert_ranges_to_str, get_color, get_distance_history,
                     get_last_day_of_month, get_week_range, get_weekly_rides,
                     get_weekly_sums)


@login_required
def dashboard(request):
    user = request.user
    units_display_preference = user.profile.units_display_preference
    unit_names = get_unit_names(units_display_preference)
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

    if units_display_preference == "imperial":
        week = convert_to_imperial(week, "dashboard_week")
        data = convert_to_imperial(data, "dashboard_data")

    # build chart_title
    if units_display_preference == "imperial":
        chart_title = "Distance (miles) by week"
    else: # metric
        chart_title= "Distance (km) by week"

    context = {
        "week": week,
        "labels": labels,
        "data": data,
        "unit_names": unit_names,
        "chart_title": chart_title,
    }

    return render(request, "dashboard/dashboard.html", {"context": context})


@login_required
def db_month(request):
    if request.method == "POST":
        form = DBMonthForm(request.POST)
        if form.is_valid():
            start_year = form.cleaned_data["start_year"]
            end_year = form.cleaned_data["end_year"]
            range_override = True
    else:
        form = DBMonthForm(
            initial={
                "start_year": datetime.datetime.now().year - 5,
                "end_year": datetime.datetime.now().year,
            }
        )
        range_override = False

    colors = [
        "#827BC5",
        "#7D8B96",
        "#15807C",
        "#332F32",
        "#C8C1BB",
        "#AB4738",
        "#5B5963",
    ]

    earliest_ride = Doc.objects.filter(user=request.user, active=True).earliest()
    start_date = earliest_ride.doc_date
    first_date = start_date.replace(day=1)

    # if first_date is more then 5 years ago, change first_date to 5 years ago
    # too keep chart from having too much data to view easily
    if first_date.year < datetime.datetime.now().year - 5:
        tz = get_localzone()
        first_date = tz.localize(
            datetime.datetime(datetime.datetime.now().year - 5, 1, 1)
        )

    last_date = datetime.datetime.now(timezone.utc)

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
            last_date = datetime.datetime(
                end_year, current_month, current_month_end_day
            )
        else:
            last_date = datetime.datetime(end_year, 12, 31)

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=first_date, until=last_date):
        year = str(dt.strftime("%Y"))
        month = str(dt.strftime("%m"))
        month_year_str = str(dt.strftime("%b %Y"))
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
            doc_date__year=year,
            doc_date__month=month,
            active=True,
            doc_type="ride",
        )
        for ride in rides:
            miles_this_year += ride.data["distance"]
        milage.append(round(miles_this_year))

    print(milage)
    units_display_preference = request.user.profile.units_display_preference
    if units_display_preference == "imperial":
        chart_title = "Distance (miles) by month"
        milage = convert_to_imperial(milage, "dashboard_data")
    else: # metric
        chart_title= "Distance (km) by month"



    context = {
        "form": form,
        "labels": month_year,
        "data": milage,
        "bgColor": bgColor,
        "chart_title": chart_title,
    }

    return render(request, "dashboard/month.html", {"context": context})


class db_year(LoginRequiredMixin, TemplateView):
    colors = [
        "#827BC5",
        "#7D8B96",
        "#15807C",
        "#332F32",
        "#C8C1BB",
        "#AB4738",
        "#5B5963",
    ]
    template_name = "dashboard/year.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        earliest_ride = Doc.objects.filter(
            user=self.request.user, active=True
        ).earliest()
        start = int(earliest_ride.doc_date.strftime("%Y"))
        current = datetime.date.today().year

        years = []
        milage = []
        bgColor = []

        for i, year in enumerate(range(start, current + 1)):
            years.append(year)
            bgColor.append(get_color(self.colors, i))

            # get yearly milage
            miles_this_year = 0
            rides = Doc.objects.filter(
                user=self.request.user,
                doc_date__year=year,
                active=True,
                doc_type="ride",
            )
            for ride in rides:
                miles_this_year += ride.data["distance"]
            milage.append(round(miles_this_year))

        context["labels"] = years
        context["data"] = milage
        context["bgColor"] = bgColor
        context["chart_title"] = "Distance (KM) by Year"
        return context


class dbnew(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/db2.html"
    model = Doc
    context_object_name = "chart"

    def get_template_names(self):
        chart_type = self.request.GET.get('chart_type')
        print("*****gtn: chart_type: ", chart_type, type(chart_type))
        if self.request.htmx: # get partial while using htmx get request
            print("_chart.html")
            return "dashboard/_chart.html"
        else:
            print("db2.html")
            return "dashboard/db2.html"

    def get_context_data(self, **kwargs):
        context = {}
        chart_type = self.request.GET.get('chart_type')
        context["chart_type"] = chart_type
        print("chart_type: ", chart_type, type(chart_type))

        if chart_type == "weekly" or chart_type == None:
            print("weekly****")
            user = self.request.user

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

            context["week"] = week
            context["labels"] = labels
            context["data"] = data

        elif chart_type == "monthly":
            print("monthly****")
            labels = {}
            data = {}
        elif chart_type == "yearly":
            print("yearly****")
            labels = {}
            data = {}
        else:
            print("else****")
            labels = {}
            data = {}

        print("context: ", context)

        return context

