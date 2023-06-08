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

    # Get template for partial page when using htmx scrolling
    def get_template_names(self):
        if self.request.htmx: # get partial while using htmx scrolling
            return "feed/_activities.html"

        return "feed/feed.html" # get full page on initial load


    # Get queryset for feed
    def get_queryset(self):
        user=self.request.user

        queryset = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp") | Doc.objects.filter(user=user, doc_type="joined")
        queryset = queryset.order_by("-doc_date")

        for activity in queryset:
            if activity.doc_type == "ride":
                activity.map = build_map(activity)
            activity.data = clean_data_for_display(activity.data)

        return queryset


    # Get extra context for user info
    def get_context_data(self,**kwargs):
        context = super(FeedView,self).get_context_data(**kwargs)
        user=self.request.user

        member_joined_date = Doc.objects.filter(user=user, doc_type="joined").values('doc_date')
        member_joined_date = member_joined_date[0]['doc_date']
        member_joined_date = member_joined_date.strftime("%B %d, %Y")
        context["member_joined_date"]=member_joined_date

        activities_total = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp") | Doc.objects.filter(user=user, doc_type="joined")
        activities_total = activities_total.count()
        context["activities_total"]=activities_total

        activities_ride = Doc.objects.filter(user=user, doc_type="ride").count()
        context["activities_ride"]=activities_ride

        return context


class DetailView(LoginRequiredMixin, DetailView):
    template_name = "feed/detail.html"
    model = Doc

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        chart = {}

        doc_id = self.kwargs["pk"]
        doc = Doc.objects.get(id=doc_id)

        activity = clean_data_for_display(doc.data)
        activity_type = doc.doc_type
        if activity_type == "ride":
            activity["map"] = build_map(doc)

            chart["labels"] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
            chart["elevation"] = [100, 101, 103, 107, 110, 109, 108, 106, 103, 102, 101, 100, 100]

        context["chart"] = chart
        context["doc_type"] = doc.doc_type
        context["activity"] = activity

        return context
