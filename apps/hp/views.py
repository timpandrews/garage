from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from apps.garage.models import Doc

from .forms import GenericHPForm, WeightHPForm, BPHPForm


class HPBaseView(View):
    model = Doc
    success_url = reverse_lazy('hp:list')


class HPListView(LoginRequiredMixin, HPBaseView, ListView):
    template_name = 'hp/hp_list.html'
    context_object_name = "hps"
    paginate_by = 20

    def get_queryset(self):
        hps = self.model.objects.order_by("-id").filter(
            doc_type="hp", user=self.request.user, active=True
        )

        return hps


class HPDetailView(LoginRequiredMixin, HPBaseView, DetailView):
    fields = "__all__"
    template_name = "hp/hp_detail.html"


class HPCreateView(LoginRequiredMixin, HPBaseView, CreateView):
    form_class = GenericHPForm
    template_name = "hp/hp_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        data = build_data_value(form.cleaned_data)
        doc_date = datetime.now()
        self.object = Doc(doc_type="hp", doc_date=doc_date, user=user, data=data)
        self.object.save()

        return_to = self.request.GET.get('return_to', '')
        if return_to == "feed":
            return redirect("/feed/")
        else:
            return redirect(self.get_success_url())

    def get_form_class(self):
        form_class = set_form_class(self.kwargs)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["display_pref"] = user.profile.units_display_preference
        return context


class HPUpdateView(LoginRequiredMixin, HPBaseView, UpdateView):
    form_class = GenericHPForm
    template_name = "hp/hp_form.html"

    def get_initial(self):
        hp = self.get_object()
        return hp.data

    def get_form_class(self):
        form_class = set_form_class(self.kwargs)
        return form_class

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        data = build_data_value(form.cleaned_data)
        doc_date = self.object.doc_date
        self.object.data = data
        self.object.save()

        return_to = self.request.GET.get('return_to', '')
        if return_to == "feed":
            return redirect("/feed/")
        else:
            return redirect(self.get_success_url())


class HPDeleteView(LoginRequiredMixin, HPBaseView, DeleteView):
    template_name = "hp/hp_confirm_delete.html"


def set_form_class(kwargs):
    """Defines the form to be used based on the hp_type.

    Args:
        kwargs (_type_): optional argument passed to the view

    Returns:
        _type_: the form class to be used
    """
    if 'hp_type' in kwargs:
        hp_type = kwargs['hp_type']
    else:
        hp_type = 'generic'

    if hp_type == 'generic':
        form_class = GenericHPForm
    elif hp_type == 'weight':
        form_class = WeightHPForm
    elif hp_type == 'bp':
        form_class = BPHPForm
    elif hp_type == 'other':
        form_class = GenericHPForm

    return form_class


def build_data_value(data):
    """Build the json value for the data field.

    Args:
        data (_type_): form.cleaned_data

    Returns:
        _type_: json value for the data field
    """
    data_value = {}
    for key, value in data.items():
        # if value is a dict called data then update the data_value dict
        # this accounts for the "other" type and the GenericHPForm
        if key == 'data':
            data_value.update(value)
        # else if value a single value then append that key/value pair to the data_value dict
        else:
            data_value[key] = value

    return data_value