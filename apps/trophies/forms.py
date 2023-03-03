from django import forms

from apps.garage.models import Profile


class TrophiesForm(forms.ModelForm):
    # trophies = forms.CharField(
    #     required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['trophies',]