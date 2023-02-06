from django.http import HttpResponseRedirect
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


class RideListView(RideBaseView, ListView):
    """View to list all rides.
    Use the 'ride_list' variable in the template
    to access all Ride objects"""
    fields = '__all__'
    queryset = Doc.objects.filter(data_type="ride").order_by('-id')
    template_name = "rides/ride_list.html"
    context_object_name = 'rides'
    paginate_by = 5


class RideDetailView(RideBaseView, DetailView):
    """View to list the details from one ride.
    Use the 'ride' variable in the template to access
    the specific ride here and in the Views below"""
    fields = '__all__'
    template_name = "rides/ride_detail.html"


class RideCreateView(RideBaseView, CreateView):
    """View to create a new ride"""
    template_name = "rides/ride_form.html"
    form_class = AddNewRide

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print("******here******")
        user_id = 1  # placeholder for user table
        data = form.cleaned_data
        data["duration"] = data["duration"].total_seconds()
        self.object = Doc(data_type="ride", user_id=user_id, data=data)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class RideUpdateView(RideBaseView, UpdateView):
    """View to update a ride"""
    form_class = AddNewRide
    # fields = "__all__"
    template_name = "rides/ride_form.html"

    def get_initial(self):
        ride = self.get_object()
        print(ride.data)
        return ride.data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print("******here******")
        user_id = 1  # placeholder for user table
        data = form.cleaned_data
        data["duration"] = data["duration"].total_seconds()
        self.object = Doc(data_type="ride", user_id=user_id, data=data)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class RideDeleteView(RideBaseView, DeleteView):
    """View to delete a ride"""
    template_name = "rides/ride_confirm_delete.html"