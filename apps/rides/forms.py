from django import forms
from django.forms import ModelForm

from apps.garage.models import Doc


class AddNewRide(ModelForm):
    start = forms.DateTimeField(
        label="Start Time/Day", help_text="%Y-%m-%d%H:%M:%S", initial="2023-02-09 11:02:00"
    )
    ride_title = forms.CharField(
        label="Ride Title", max_length=200, initial="Ride Title Test"
    )
    route = forms.CharField(label="Route", max_length=200, initial="Route Info")
    equipment = forms.CharField(
        label="Equipment", max_length=200, initial="Info about your bike, trainer, etc."
    )
    notes = forms.CharField(label="Notes", max_length=200, initial="Notes")
    distance = forms.FloatField(label="Distance", min_value=0, initial=12.3)
    duration = forms.DurationField(
        label="Ride Duration", initial="1:2:3", help_text="h:m:s"
    )
    elevation = forms.IntegerField(label="Elevation Gained", min_value=0, initial=123)
    weighted_power_avg = forms.IntegerField(label="Weighted Power Average", min_value=0, initial=123)
    total_work = forms.IntegerField(label="Total Work", min_value=0, initial=123)
    speed_avg = forms.FloatField(label="Average Speed", min_value=0, initial=12.3)
    speed_max = forms.FloatField(label="Max Speed", min_value=0, initial=12.3)
    hr_avg = forms.IntegerField(label="Average Heart Rate", min_value=0, initial=123)
    hr_max = forms.IntegerField(label="Max Heart Rate", min_value=0, initial=123)
    cadence_avg = forms.IntegerField(label="Average Cadence", min_value=0, initial=123)
    cadence_max = forms.IntegerField(label="Max Cadence", min_value=0, initial=123)
    power_avg = forms.IntegerField(label="Average Power", min_value=0, initial=123)
    power_max = forms.IntegerField(label="Max Power", min_value=0, initial=123)
    calories = forms.IntegerField(label="Calories", min_value=0, initial=123)

    class Meta:
        model = Doc
        exclude = ["user", "data_type", "data"]
