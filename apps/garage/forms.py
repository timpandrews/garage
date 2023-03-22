from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            ]


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(
        max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    location = forms.CharField(
        max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    birth_date = forms.DateField(
        required=False, widget=DatePickerInput(attrs={"class": "form-control"}))
    profile_pic = forms.ImageField(
        label="Profile Picture",
        required=False
    )
    strava_url = forms.CharField(
        label="Strava Profile URL",
        max_length=200,
        required=False,
    )
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_pic', 'strava_url',]