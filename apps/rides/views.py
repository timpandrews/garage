from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.garage.models import Doc


class RideBaseView(View):
    model = Doc
    fields = '__all__'
    success_url = reverse_lazy('rides:all') # TODO rename to all_rides


class RideListView(RideBaseView, ListView):
    """View to list all rides.
    Use the 'ride_list' variable in the template
    to access all Ride objects"""
    queryset = Doc.objects.filter(data_type="ride").order_by('-id')
    template_name = "rides/ride_list.html"
    context_object_name = 'rides'
    paginate_by = 5


class RideDetailView(RideBaseView, DetailView):
    """View to list the details from one ride.
    Use the 'ride' variable in the template to access
    the specific ride here and in the Views below"""
    template_name = "rides/ride_detail.html"
    extra_context = {"extra": Doc.objects.filter(id=10)}


class RideCreateView(RideBaseView, CreateView):
    """View to create a new ride"""
    template_name = "rides/ride_form.html"


class RideUpdateView(RideBaseView, UpdateView):
    """View to update a ride"""
    template_name = "rides/ride_form.html"


class RideDeleteView(RideBaseView, DeleteView):
    """View to delete a ride"""
    template_name = "rides/ride_confirm_delete.html"