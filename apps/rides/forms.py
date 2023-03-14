from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from django.forms import ModelForm

from apps.garage.models import Doc


class RideForm(ModelForm):
    # "%Y-%m-%d %H:%M:%S"
    start = forms.DateTimeField(
        required=True,
        widget=DateTimePickerInput(attrs={"class": "form-control"}),
    )
    ride_title = forms.CharField(
        label="Ride Title",
        max_length=200,
        required=False,
    )
    route = forms.CharField(
        label="Route",
        max_length=200,
        required=False
    )
    equipment = forms.CharField(
        label="Equipment",
        max_length=200,
        required=False,
    )
    notes = forms.CharField(
        label="Notes",
        max_length=200,
        required=False,
    )
    distance = forms.FloatField(
        label="Distance",
        min_value=0,
        required=True,
    )
    duration = forms.DurationField(
        label="Ride Duration",
        help_text="h:m:s",
        required=True,
    )
    elevation = forms.IntegerField(
        label="Elevation Gained",
        min_value=0,
        required=False,
    )
    weighted_power_avg = forms.IntegerField(
        label="Weighted Power Average",
        min_value=0,
        required=False,
    )
    total_work = forms.IntegerField(
        label="Total Work",
        min_value=0,
        required=False,
    )
    speed_avg = forms.FloatField(
        label="Average Speed",
        min_value=0,
        required=False,
    )
    speed_max = forms.FloatField(
        label="Max Speed",
        min_value=0,
        required=False,
    )
    hr_avg = forms.IntegerField(
        label="Average Heart Rate",
        min_value=0,
        required=False,
    )
    hr_max = forms.IntegerField(
        label="Max Heart Rate",
        min_value=0,
        required=False,
    )
    cadence_avg = forms.IntegerField(
        label="Average Cadence",
        min_value=0,
        required=False,
    )
    cadence_max = forms.IntegerField(
        label="Max Cadence",
        min_value=0,
        required=False,
    )
    power_avg = forms.IntegerField(
        label="Average Power",
        min_value=0,
        required=False,
    )
    power_max = forms.IntegerField(
        label="Max Power",
        min_value=0,
        required=False,
    )
    calories = forms.IntegerField(
        label="Calories",
        min_value=0,
        required=False,
    )
    fitfile = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
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
            "fit_data",
            "gpx_data",
        )
