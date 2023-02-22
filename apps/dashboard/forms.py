import datetime
import re

from django import forms
from django.forms import Form
from django.forms.widgets import Select, Widget, SelectDateWidget
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

YEAR_CHOICES = [
    ('2011', 2011),
    ('2012', 2012),
    ('2013', 2013),
    ('2014', 2014),
    ('2015', 2015),
    ('2016', 2016),
    ('2017', 2017),
    ('2018', 2018),
    ('2019', 2019),
    ('2020', 2020),
    ('2021', 2021),
    ('2022', 2022),
    ('2023', 2023),
]

class DBMonthForm(Form):
    start_year = forms.IntegerField(
        label="Start",
        required=False,
        widget=forms.Select(choices=YEAR_CHOICES),
    )
    end_year = forms.IntegerField(
        label="End",
        required=False,
        widget=forms.Select(choices=YEAR_CHOICES),
    )









