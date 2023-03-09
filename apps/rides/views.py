from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.garage.models import Doc

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
