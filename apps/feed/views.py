from common.tools import (
    build_elevation_chart,
    build_map,
    clean_data_for_display,
    convert_to_imperial,
    get_unit_names,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from apps.garage.models import Doc


class FeedView(LoginRequiredMixin, ListView):
    template_name = "feed/feed.html"
    context_object_name = "feed"
    model = Doc
    paginate_by = 10

    # Get template for partial page when using htmx scrolling
    def get_template_names(self):
        if self.request.htmx:  # get partial while using htmx scrolling
            return "feed/activities/_activities.html"

        return "feed/feed.html"  # get full page on initial load

    # Get queryset for feed
    def get_queryset(self):
        user = self.request.user

        queryset = (
            Doc.objects.filter(user=user, doc_type="ride")
            | Doc.objects.filter(user=user, doc_type="hp")
            | Doc.objects.filter(user=user, doc_type="joined")
            | Doc.objects.filter(user=user, doc_type="habit")
        )
        queryset = queryset.order_by("-doc_date")

        for activity in queryset:
            if activity.doc_type == "ride":
                activity.map = build_map(activity)

            activity.data = clean_data_for_display(activity.data)

            if user.profile.units_display_preference == "imperial":
                activity.data = convert_to_imperial(activity.data, activity.doc_type)

        return queryset

    # Get extra context for user info
    def get_context_data(self, **kwargs):
        context = super(FeedView, self).get_context_data(**kwargs)
        user = self.request.user

        member_joined_date = Doc.objects.filter(user=user, doc_type="joined").values(
            "doc_date"
        )
        member_joined_date = member_joined_date[0]["doc_date"]
        member_joined_date = member_joined_date.strftime("%B %d, %Y")
        context["member_joined_date"] = member_joined_date

        activities_total = (
            Doc.objects.filter(user=user, doc_type="ride")
            | Doc.objects.filter(user=user, doc_type="hp")
            | Doc.objects.filter(user=user, doc_type="joined")
            | Doc.objects.filter(user=user, doc_type="habit")
        )
        activities_total = activities_total.count()
        context["activities_total"] = activities_total

        activities_ride = Doc.objects.filter(user=user, doc_type="ride").count()
        context["activities_ride"] = activities_ride

        context["display_pref"] = user.profile.units_display_preference
        context["unit_names"] = get_unit_names(user.profile.units_display_preference)

        return context


class DetailView(LoginRequiredMixin, DetailView):
    template_name = "feed/detail.html"
    model = Doc

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        user_display_pref = user.profile.units_display_preference

        chart = {}

        doc_id = self.kwargs["pk"]
        doc = Doc.objects.get(id=doc_id)

        activity = clean_data_for_display(doc.data)

        activity_type = doc.doc_type

        if user_display_pref == "imperial":
            activity = convert_to_imperial(activity, activity_type)

        if activity_type == "ride":
            activity["map"] = build_map(doc)
            chart["labels"], chart["elevation"] = build_elevation_chart(
                doc, user.profile.units_display_preference
            )

        if user.profile.units_display_preference == "imperial":
            chart["y_label"] = "Distance (miles)"
            chart["x_label"] = "Elevation (ft)"
        else:  # metric
            chart["y_label"] = "Distance (km)"
            chart["x_label"] = "Elevation (m)"

        context["chart"] = chart

        context["doc_type"] = doc.doc_type
        context["activity"] = activity

        context["display_pref"] = user.profile.units_display_preference
        context["unit_names"] = get_unit_names(user.profile.units_display_preference)

        context["kudos"] = getKudos(doc, user_display_pref)
        print(context)

        return context


def getKudos(doc, user_display_pref):
    """
    Calculate the kudos based on the distance and user display preference.  Other
    kudos may be added in the future.

    Args:
        doc (dict): The document containing the data.
        user_display_pref (str): The user's display preference ("imperial" or "metric").

    Returns:
        dict: A dictionary containing the calculated kudos.
    """
    kudos = dict()

    if user_display_pref == "imperial":
        beats = doc.data["distance"] * 20
    else: # if metric of no preference (metric is default)
        user_display_pref == "metric"
        beats = round(doc.data["distance"] * 32.1869)

    kudos["beats"] = beats

    return kudos
        