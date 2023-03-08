from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from apps.garage.models import Doc

from .forms import GenericHPForm


class HPBaseView(View):
    model = Doc
    success_url = reverse_lazy('hp:all')


class HPListView(LoginRequiredMixin, HPBaseView, ListView):
    print('HPListView')
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
        data = form.cleaned_data["data"]
        doc_date = datetime.now()
        self.object = Doc(doc_type="hp", doc_date=doc_date, user=user, data=data)
        self.object.save()

        return redirect(self.get_success_url())


class HPUpdateView(LoginRequiredMixin, HPBaseView, UpdateView):
    form_class = GenericHPForm
    template_name = "hp/hp_form.html"


class HPDeleteView(LoginRequiredMixin, HPBaseView, DeleteView):
    template_name = "hp/hp_confirm_delete.html"











