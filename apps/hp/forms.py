from django import forms

from apps.garage.models import Doc


class GenericHPForm(forms.ModelForm):
    type = forms.CharField(
        widget=forms.HiddenInput(),
        initial="other",
    )
    class Meta:
        model = Doc
        fields = ["type", "data"]
        widgets = {
            "data": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "cols": 50,
                    "placeholder": "Enter your data here",
                }
            )
        }


class WeightHPForm(forms.ModelForm):
    type = forms.CharField(
        widget=forms.HiddenInput(),
        initial="weight",
    )
    weight = forms.IntegerField(
        label="Weight",
        min_value=0,
    )

    class Meta:
        model = Doc
        exclude = (
            "user",
            "doc_type",
            "doc_date",
            "data",
            "fit_data",
            "gpx_data",
            "active",
            "kudosed",
        )


class BPHPForm(forms.ModelForm):
    type = forms.CharField(
        widget=forms.HiddenInput(),
        initial="bp",
    )
    bp_STOL = forms.IntegerField(
        label="Systolic",
        min_value=0,
    )
    bp_DTOL = forms.IntegerField(
        label="Diastolic",
        min_value=0,
    )

    class Meta:
        model=Doc
        exclude = (
            "user",
            "doc_type",
            "doc_date",
            "data",
            "fit_data",
            "gpx_data",
            "active",
            "kudosed",
        )
