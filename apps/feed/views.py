from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.garage.models import Doc


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = "feed/feed.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FeedView, self).get_context_data(*args, **kwargs)

        user=self.request.user
        feed = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp")
        feed = feed.order_by("-doc_date")
        context["feed"] = feed

        return context


class DetailView(LoginRequiredMixin, TemplateView):
    template_name = "feed/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        doc_id = self.kwargs["doc_id"]
        doc = Doc.objects.get(id=doc_id)


        context["doc_type"] = doc.doc_type
        context["doc"] = doc

        return context