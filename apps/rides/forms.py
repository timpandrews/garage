from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminSplitDateTime

from apps.garage.models import Doc


class AddNewRide(ModelForm):
    start = forms.SplitDateTimeField(
        label="Start Date/Time", widget=AdminSplitDateTime()
    )  # "%Y-%m-%d %H:%M:%S"
    ride_title = forms.CharField(
        label="Ride Title",
        max_length=200,
        required=False,
    )
    route = forms.CharField(label="Route", max_length=200, required=False)
    equipment = forms.CharField(
        label="Equipment",
        max_length=200,
        required=False,
    )
    notes = forms.CharField(label="Notes", max_length=200, required=False)
    distance = forms.FloatField(
        label="Distance",
        min_value=0,
    )
    duration = forms.DurationField(label="Ride Duration", help_text="h:m:s")
    elevation = forms.IntegerField(
        label="Elevation Gained",
        min_value=0,
    )
    weighted_power_avg = forms.IntegerField(
        label="Weighted Power Average",
        min_value=0,
    )
    total_work = forms.IntegerField(
        label="Total Work",
        min_value=0,
    )
    speed_avg = forms.FloatField(
        label="Average Speed",
        min_value=0,
    )
    speed_max = forms.FloatField(
        label="Max Speed",
        min_value=0,
    )
    hr_avg = forms.IntegerField(
        label="Average Heart Rate",
        min_value=0,
    )
    hr_max = forms.IntegerField(
        label="Max Heart Rate",
        min_value=0,
    )
    cadence_avg = forms.IntegerField(
        label="Average Cadence",
        min_value=0,
    )
    cadence_max = forms.IntegerField(
        label="Max Cadence",
        min_value=0,
    )
    power_avg = forms.IntegerField(
        label="Average Power",
        min_value=0,
    )
    power_max = forms.IntegerField(
        label="Max Power",
        min_value=0,
    )
    calories = forms.IntegerField(
        label="Calories",
        min_value=0,
    )

    class Meta:
        model = Doc
        exclude = (
            "user",
            "doc_type",
            "doc_date",
            "data",
            "active",
            "kudosed",
        )
