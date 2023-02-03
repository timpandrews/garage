from django import forms
from django.forms import ModelForm
from .models import Doc


class AddNewRide(ModelForm):
    ride_title = forms.CharField(
        label="Ride Title", max_length=200, initial="Ride Title Test"
    )
    distance = forms.FloatField(label="Distance", min_value=0, initial=12.3)
    calories = forms.IntegerField(label="Calories", min_value=0, initial=123)

    class Meta:
        model = Doc
        fields = ["ride_title", "distance", "calories"]
