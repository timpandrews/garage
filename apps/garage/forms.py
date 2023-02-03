from django import forms
from django.forms import ModelForm
from .models import Doc

class AddNewRide(ModelForm):

    extra_field = forms.CharField()

    class Meta:
        model = Doc
        fields = ['title', 'extra_field']

