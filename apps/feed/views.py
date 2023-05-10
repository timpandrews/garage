from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.garage.models import Doc


@login_required
def feed(request):

    user = request.user

    # get docs where user is current user and doc type = ride and sort by doc_date
    feed = Doc.objects.filter(user=user, doc_type="ride") | Doc.objects.filter(user=user, doc_type="hp")
    feed = feed.order_by("-doc_date")
    print(feed)

    context = {
        "user": user,
        "feed": feed,
    }

    return render(request, "feed/feed.html", context)

