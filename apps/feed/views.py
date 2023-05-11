from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.garage.models import Doc


class FeedView(LoginRequiredMixin, ListView):
    template_name = "feed/feed.html"
    context_object_name = "feed"
    model = Doc
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return "feed/_activities.html"

        return "feed/feed.html"

    def get_queryset(self):
        user=self.request.user
        print("user", user)
        queryset = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp")
        queryset = queryset.order_by("-doc_date")
        print("queryset", queryset)

        return queryset

    # def get_context_data(self, *args, **kwargs):
    #     context = super(FeedView, self).get_context_data(*args, **kwargs)

    #     user=self.request.user
    #     feed = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp")
    #     feed = feed.order_by("-doc_date")
    #     context["feed"] = feed

    #     return context


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