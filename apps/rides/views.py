from datetime import datetime, timedelta

import fitdecode
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.garage.models import Doc
from common.tools import import_fit_file

from .forms import RideForm


class RideBaseView(View):
    model = Doc
    success_url = reverse_lazy("rides:all")


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
        earliest_ride = Doc.objects.filter(
            user=self.request.user, active=True
        ).earliest()
        earliest_date = earliest_ride.doc_date.strftime("%B %Y")
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


class RideCreateView(LoginRequiredMixin, RideBaseView, CreateView):
    template_name = "rides/ride_form.html"
    form_class = RideForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        data = form.cleaned_data
        data = clean_data_for_db(data)
        doc_date = data["start"]
        doc_date = datetime.strptime(doc_date, "%m/%d/%Y %H:%M:%S")
        self.object = Doc(doc_type="ride", doc_date=doc_date, user=user, data=data)
        self.object.save()

        return redirect(self.get_success_url())


class RideUpdateView(LoginRequiredMixin, RideBaseView, UpdateView):
    form_class = RideForm
    template_name = "rides/ride_form.html"

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
        self.object.date_date = doc_date
        self.object.data = data
        self.object.save()

        return redirect(self.get_success_url())


class RideDeleteView(LoginRequiredMixin, RideBaseView, DeleteView):
    template_name = "rides/ride_confirm_delete.html"


def ride_import_fit(request):
    context = {}

    if request.method == "POST":
        uploaded_file = request.FILES['fit_file'] if 'fit_file' in request.FILES else None

        if uploaded_file: # check if file was uploaded
            #check if file was uploaded
            if not uploaded_file:
                print("****** No file uploaded")

            # check file extension to make sure it's a FIT file
            if uploaded_file.name[-4:] == ".fit":
                fs = FileSystemStorage()
                fit_file = fs.save(uploaded_file.name, uploaded_file)
                fit_file_path = fs.path(fit_file)
                messages.success(request, "You have upload the file: " + uploaded_file.name)
                context["uploaded_file_name"] = uploaded_file.name

                # read FIT file
                fit_file_data = import_fit_file(fit_file_path)

                # delete file from media directory after reading
                fs.delete(fit_file)
                
                print(fit_file_data["file_id"][0]["manufacturer"])

            else:
                messages.error(
                    request,
                    "Sorry we couldn't upload that file.  The file must be a .fit file.  "
                    "Please select a .fit file and try again."
                )
        else: # no file uploaded
            messages.error(request, "No file uploaded, please select a file to upload")



    return render(request, "rides/ride_import_fit.html", context)


def clean_data_for_db(data):
    # convert H:M:S duration field to total seconds
    data["duration"] = data["duration"].total_seconds()
    # convert datetime object to string to stor in JSON
    data["start"] = data["start"].strftime("%m/%d/%Y %H:%M:%S")

    return data


def clean_data_for_display(data):
    # convert duration field from seconds to H:M:S format
    data["duration"] = str(timedelta(seconds=data["duration"]))

    return data


def clean_data_for_edit(data):
    # convert duration field from seconds to H:M:S format
    data["duration"] = str(timedelta(seconds=data["duration"]))
    # convert datetime string to datetime object for datetime formfield
    data["start"] = datetime.strptime(data["start"], "%m/%d/%Y %H:%M:%S")

    return data
