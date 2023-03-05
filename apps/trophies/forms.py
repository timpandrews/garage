from django import forms

from apps.garage.models import Profile


class TrophiesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["trophies"]
