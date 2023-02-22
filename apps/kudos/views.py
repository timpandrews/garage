from django.shortcuts import render


def kudos(request):
    context = {}

    return render(request, "kudos/kudos.html", {'context': context})


def trophies(request):
    context = {}

    return render(request, "kudos/trophies.html", {'context': context})