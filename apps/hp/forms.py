from django import forms

from apps.garage.models import Doc


class GenericHPForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = ["data"]
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

