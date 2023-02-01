from django import forms


class AddRide(forms.Form):
    title = forms.CharField(max_length=200)
    text = forms.TextField()

