import folium
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.garage.models import Doc


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

        queryset = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp")
        queryset = queryset.order_by("-doc_date")

        for activity in queryset:
            if activity.doc_type == "ride":
                activity.map = build_map(activity)
                
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


def find_centroid(coordinates):
    """
    Given a list of coordinates (lat/long), will return the centroid (center point)

    Args:
        coordinates (list): A list of tuple pairs of Latitudes and Longitudes.
        Example: [(lat1, long1), (lat2, long2), ...]
        Latitutdes and Logitudes must be floats

    Returns:
        tuple: Returns a tuple of the centroid (lat, long) of the coordinates of
        the center point of the given coordinates.  For example: (lat, long) where
        lat and long are floats.
    """
    x = [float(x) for x, y in coordinates]
    y = [float(y) for x, y in coordinates]
    centroid = (sum(x) / len(coordinates), sum(y) / len(coordinates))

    return centroid


def build_map(activity):
    """
    Given an activity (ride with coordinates), will build a map of the route
    using the folium library.  Map will take coordinatres and build a polyline
    of the route.  Map will be centered on the centroid of the route.

    Args:
        activity (dict): Activity is a dict of the ride data.  It includes meta
        data about the ride/activity as well as data from the .fit file including
        the coordinates of the route.

    Returns:
        *if coordinates are available*
        folium map object: Returns a folium map object that can be rendered as html
        in a template..

        *if no coordinates are available*
        string: Returns a string that says "No Map Data" when the map cannot be
        built.

    """
    try:
        route = []
        for record in activity.fit_data["record"]:
            # This is the semicircles to/from degrees calc.
            #     degrees = semicircles * ( 180 / 2^31 )
            #     semicircles = degrees * ( 2^31 / 180 )
            lat = record["position_lat"] * 180 / 2 ** 31
            long = record["position_long"] * 180 / 2 ** 31
            coordinates = (lat, long)
            route.append(coordinates)

        centroid = find_centroid(route)
        m = folium.Map(
            location=[centroid[0], centroid[1]],
            zoom_start=13,
            tiles='OpenStreetMap',
        )
        folium.PolyLine(route).add_to(m)
        return m._repr_html_()

    except Exception as e:
        return "No Map Data"