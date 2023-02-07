from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.garage.models import Doc

from .forms import AddNewRide


class RideBaseView(View):
    model = Doc
    success_url = reverse_lazy('rides:all') # TODO rename to all_rides


class RideListView(RideBaseView, ListView, LoginRequiredMixin):
    print('*******')
    fields = '__all__'
    # queryset = Doc.objects.filter(user=self.request.user).order_by('-id')
    template_name = "rides/ride_list.html"
    context_object_name = 'rides'
    paginate_by = 5

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        return qs.filter(data_type="ride", user=self.request.user)

class RideDetailView(RideBaseView, DetailView, LoginRequiredMixin):
    fields = '__all__'
    template_name = "rides/ride_detail.html"


class RideCreateView(RideBaseView, CreateView, LoginRequiredMixin):
    template_name = "rides/ride_form.html"
    form_class = AddNewRide

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        data = form.cleaned_data
        data["duration"] = data["duration"].total_seconds()
        self.object = Doc(data_type="ride", user=user, data=data)
        self.object.save()

        return redirect(self.get_success_url())


class RideUpdateView(RideBaseView, UpdateView, LoginRequiredMixin):
    form_class = AddNewRide
    # fields = "__all__"
    template_name = "rides/ride_form.html"

    def get_initial(self):
        ride = self.get_object()
        return ride.data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        data = form.cleaned_data
        # print('*******')
        # doc_id = self.get_object().id
        data["duration"] = data["duration"].total_seconds()
        self.object.data = data
        self.object.save()

        return redirect(self.get_success_url())


class RideDeleteView(RideBaseView, DeleteView, LoginRequiredMixin):
    """View to delete a ride"""
    template_name = "rides/ride_confirm_delete.html"