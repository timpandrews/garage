from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.garage.models import Doc
from common.tools import clean_data_for_display, build_map


class FeedView(LoginRequiredMixin, ListView):
    template_name = "feed/feed.html"
    context_object_name = "feed"
    model = Doc
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx: # get partial while using htmx scrolling
            return "feed/_activities.html"

        return "feed/feed.html" # get full page on initial load

    def get_queryset(self):
        user=self.request.user

        queryset = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp") | Doc.objects.filter(user=user, doc_type="joined")
        queryset = queryset.order_by("-doc_date")

        for activity in queryset:
            if activity.doc_type == "ride":
                activity.map = build_map(activity)
            activity.data = clean_data_for_display(activity.data)


        return queryset


class DetailView(LoginRequiredMixin, DetailView):
    template_name = "feed/detail.html"
    model = Doc

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        doc_id = self.kwargs["pk"]
        doc = Doc.objects.get(id=doc_id)

        context["doc_type"] = doc.doc_type
        context["doc"] = doc

        return context
