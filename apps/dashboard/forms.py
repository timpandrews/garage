from django import forms
from django.forms import Form

YEAR_CHOICES = [
    ("2011", 2011),
    ("2012", 2012),
    ("2013", 2013),
    ("2014", 2014),
    ("2015", 2015),
    ("2016", 2016),
    ("2017", 2017),
    ("2018", 2018),
    ("2019", 2019),
    ("2020", 2020),
    ("2021", 2021),
    ("2022", 2022),
    ("2023", 2023),
]


class DBMonthForm(Form):
    start_year = forms.IntegerField(
        label="Start",
        required=True,
        widget=forms.Select(choices=YEAR_CHOICES),
    )
    end_year = forms.IntegerField(
        label="End",
        required=True,
        widget=forms.Select(choices=YEAR_CHOICES),
    )
