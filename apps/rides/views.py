import json
import os
from datetime import datetime, timedelta, timezone

import fitdecode
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.garage.models import Doc, ZwiftRouteList
from common.tools import (clean_data_for_db, clean_data_for_display,
                          clean_data_for_edit, get_detail_from_input_data,
                          get_total_work, get_weighted_average_power,
                          import_fit_file)

from .forms import RideForm


class RideBaseView(View):
    model = Doc
    success_url = reverse_lazy("rides:list")


class RideListView(LoginRequiredMixin, RideBaseView, ListView):
    fields = "__all__"
    template_name = "rides/ride_list.html"
    context_object_name = "rides"
    paginate_by = 20

    def get_queryset(self):
        rides = self.model.objects.order_by("-id").filter(
            doc_type="ride", user=self.request.user, active=True
        )

        for ride in rides:
            ride.data = clean_data_for_display(ride.data)

        return rides

    def get_context_data(self, **kwargs):
        total_rides = Doc.objects.filter(user=self.request.user, active=True).count()

        # account for users with no rides yet
        if total_rides > 0:
            earliest_ride = Doc.objects.filter(
                user=self.request.user, active=True
            ).earliest()
            earliest_date = earliest_ride.doc_date.strftime("%B %Y")
        else:
            earliest_date = "N/A"

        data = super().get_context_data(**kwargs)
        data["total_rides"] = total_rides
        data["first_ride"] = earliest_date
        return data


class RideDetailView(LoginRequiredMixin, RideBaseView, DetailView):
    fields = "__all__"
    template_name = "rides/ride_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get original context
        data = context["object"].data
        context["object"].data = clean_data_for_display(data)

        return context


class RideCreateView(LoginRequiredMixin, SuccessMessageMixin, RideBaseView, CreateView):
    template_name = "rides/ride_form.html"
    form_class = RideForm
    # TODO: check if success message is working
    # BUG: Require distance, elevation, and maybe some other fileds to be completed
    success_message = "Ride was created successfully"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        data = form.cleaned_data
        data = clean_data_for_db(data)

        doc_date = data["start"]
        doc_date = datetime.strptime(doc_date, "%m/%d/%Y %H:%M:%S")
        doc_date = doc_date.replace(tzinfo=timezone.utc)

        self.object = Doc(doc_type="ride", doc_date=doc_date, user=user, data=data)
        self.object.save()

        return_to = self.request.GET.get('return_to', '')
        if return_to == "feed":
            return redirect("/feed/")
        else:
            return redirect(self.get_success_url())


class RideUpdateView(LoginRequiredMixin, SuccessMessageMixin, RideBaseView, UpdateView):
    form_class = RideForm
    template_name = "rides/ride_form.html"
    # TODO: check if success message is working
    success_message = "Ride was updated successfully"

    def get_initial(self):
        ride = self.get_object()
        ride.data = clean_data_for_edit(ride.data)
        return ride.data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        data = form.cleaned_data
        data = clean_data_for_db(data)

        doc_date = data["start"]
        doc_date = datetime.strptime(doc_date, "%m/%d/%Y %H:%M:%S")
        doc_date = doc_date.replace(tzinfo=timezone.utc)

        self.object.date_date = doc_date
        self.object.data = data
        self.object.save()

        return redirect(self.get_success_url())


class RideDeleteView(LoginRequiredMixin, SuccessMessageMixin, RideBaseView, DeleteView):
    template_name = "rides/ride_confirm_delete.html"
    success_message = "Ride was deleted successfully"


@login_required
def ride_import_fit(request):
    return_to = request.GET.get('return_to', '')
    context = {}
    form = RideForm(request.POST or None)

    if request.method == "POST":
        # COMMENT - Import Fit File Form
        if "import_fit" in request.POST:
            # TODO - Do I need to check who created the file? ie Zwift, Garmin, etc
            # TODO - If so, Do I need to handle files from each source differently?
            uploaded_file = request.FILES['fit_file'] if 'fit_file' in request.FILES else None

            if uploaded_file: # check if file was uploaded
                # check file extension to make sure it's a FIT file
                if uploaded_file.name[-4:] == ".fit":
                    fs = FileSystemStorage()
                    fit_file = fs.save(uploaded_file.name, uploaded_file)
                    fit_file_path = fs.path(fit_file)
                    messages.success(request, "You have upload the file: " + uploaded_file.name)
                    context["uploaded_file_name"] = uploaded_file.name

                    # read FIT file
                    fit_file_data = import_fit_file(fit_file_path)

                    # pre populate ride form with data from FIT file
                    pre_pop_form_data = get_data_from_fit_to_pre_pop_form(
                        uploaded_file.name,
                        fit_file_data
                    )

                    # create form with pre populated data
                    form = RideForm(initial=pre_pop_form_data)
                    context["form"] = form

                else:
                    messages.error(
                        request,
                        "Sorry we couldn't upload that file.  The file must be a .fit file.  "
                        "Please select a .fit file and try again."
                    )
            else: # no file uploaded
                messages.error(request, "No file uploaded, please select a file to upload")

        # COMMENT - Create Ride from form w/ extra fit_file_data
        elif "create_ride" in request.POST:
            if form.is_valid():

                object = form.save(commit=False)
                user = request.user
                data = form.cleaned_data

                # import fit file using the fit_file_name from the form
                # and then save the fit data to the database
                fit_file_name = data["fitfile"]
                fit_file_path = settings.MEDIA_ROOT + "/" + fit_file_name
                input_data = import_fit_file(fit_file_path)
                os.remove(fit_file_path) # delete file from media directory after reading
                del data["fitfile"] # remove fit_file_name from dict

                format =  "fit"
                detail = get_detail_from_input_data(format, input_data)

                data = clean_data_for_db(data)

                doc_date = data["start"]
                doc_date = datetime.strptime(doc_date, "%m/%d/%Y %H:%M:%S")
                doc_date = doc_date.replace(tzinfo=timezone.utc)

                object = Doc(
                    doc_type = "ride",
                    doc_date = doc_date,
                    user = user,
                    data = data,
                    detail = detail)
                object.save()
                messages.success(request, "Ride was created successfully")

                if return_to == "feed":
                    return redirect("/feed/")
                else:
                    return redirect("/rides/")
            else:
                messages.error(
                        request,
                        "Sorry we couldn't process this ride.  Please check the form and try again."
                    )


    return render(request, "rides/ride_import_fit.html", context)


def get_data_from_fit_to_pre_pop_form(file_name, fit_file_data):
    ride_title = file_name.split(".fit")[0].replace("_", " ")

    # TODO This stuff is for Zwift rides only, what about other sources?
    # if fit_file_data["file_id"][0]["manufacturer"] == "zwift":
    #     print("********* Zwift ride *********")

    # Hack to fix Watopia's Waistband route name
    ride_title = ride_title.replace("Watopia s Waistband", "Watopia's Waistband")

    # TODO - It would be better to user regex to find route name and world name in ride title
    list_of_route_names = ZwiftRouteList.objects.all().values_list("route_name", flat=True)
    # loop through list of route names and check if route name is in ride title
    route_name = "Unknown"
    for route in list_of_route_names:
        if route in ride_title:
             route_name = route


    list_of_worlds_names = ZwiftRouteList.objects.values_list("world_name", flat=True).distinct()
    # loop through list of world names and check if world name is in ride title
    world_name = "Unknown"
    for world in list_of_worlds_names:
        if world in ride_title:
             world_name = world

    route = f"{route_name} in {world_name}"

    start = fit_file_data["session"][0]["start_time"].replace(" UTC", "") # FIXME - This is a hack to get the time to work

    distance = round(fit_file_data["session"][0]["total_distance"] / 1000, 2)

    duration = timedelta(seconds=fit_file_data["session"][0]["total_elapsed_time"])

    elevation = (fit_file_data["session"][0]["total_ascent"])

    # NOTE - speed is in m/s, so multiply by 3.6 to get km/h
    speed_avg = round(fit_file_data["session"][0]["avg_speed"] * 3.6, 1)
    speed_max = round(fit_file_data["session"][0]["max_speed"] * 3.6, 1)

    hr_avg = fit_file_data["session"][0]["avg_heart_rate"]

    hr_max = fit_file_data["session"][0]["max_heart_rate"]

    cadence_avg = fit_file_data["session"][0]["avg_cadence"]

    cadence_max = fit_file_data["session"][0]["max_cadence"]

    power_avg = fit_file_data["session"][0]["avg_power"]

    power_max = fit_file_data["session"][0]["max_power"]

    calories = fit_file_data["session"][0]["total_calories"]

    # get power data from fit file
    power_data = list()
    interval_data = list()
    for i, record in enumerate(fit_file_data["record"]):
        timestamp = datetime.strptime(record["timestamp"], '%Y-%m-%d %H:%M:%S %Z')
        # get timestamp from previous record and determine interval (in seconds)
        # between records
        if i > 0:
            prev_timestamp = datetime.strptime(fit_file_data["record"][i-1]["timestamp"], '%Y-%m-%d %H:%M:%S %Z')
            time_between_records = timestamp - prev_timestamp
            time_between_records = time_between_records.total_seconds()
        else:
            time_between_records = 1.0

        power_data.append(record["power"])
        interval_data.append(time_between_records)

    weighted_power_avg = get_weighted_average_power(power_data, interval_data)
    total_work = get_total_work(power_data, interval_data)

    prepend_form_data = {
        "ride_title": ride_title,
        "route": route,
        "start": start,
        "distance": distance,
        "duration": duration,
        "elevation": elevation,
        "speed_avg": speed_avg,
        "speed_max": speed_max,
        "hr_avg": hr_avg,
        "hr_max": hr_max,
        "cadence_avg": cadence_avg,
        "cadence_max": cadence_max,
        "power_avg": power_avg,
        "power_max": power_max,
        "calories": calories,
        "weighted_power_avg": weighted_power_avg,
        "total_work": total_work,
        # pass fit file name to form so the fit file can be read when
        # the form is posted and then save the data to the DB
        "fitfile": file_name,
    }

    return prepend_form_data
