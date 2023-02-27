from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.kudos.views import update_kudos


@login_required
def trophies(request):
    update_kudos(request.user)
    context = {}

    return render(request, "trophies/trophies.html", {"context": context})
