from django.shortcuts import render


def hp(response):
    return render(response, "hp/hp.html", {})