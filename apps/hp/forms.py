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
        model = Doc
        exclude = (
            "user",
            "doc_type",
            "doc_date",
            "data",
            "detail",
            "fit_data",
            "gpx_data",
            "active",
            "kudosed",
        )


class BaseWeightForm(forms.ModelForm):
    """The root form for weight forms.  Contains fields to both metric and
    imperial forms.

    Args:
        forms.ModelForm
    """

    type = forms.CharField(
        widget=forms.HiddenInput(),
        initial="weight",
    )

    class Meta:
        model = Doc
        exclude = (
            "user",
            "doc_type",
            "doc_date",
            "data",
            "detail",
            "fit_data",
            "gpx_data",
            "active",
            "kudosed",
        )


class MetricWeightForm(BaseWeightForm):
    """Child weight form for metric weights.  Inherits from BaseWeightForm.
    Adds fields that will be unique to metric weights.  Also can be used
    to add fields that are similar but are labeled with different units.

    Args:
        BaseWeightForm (class): Base class for weight forms.
    """

    weight = forms.IntegerField(
        label="Weight (kg)",
        min_value=0,
    )


class ImperialWeightForm(BaseWeightForm):
    """Child weight form for imperial weights.  Inherits from BaseWeightForm.
    Adds fields that will be unique to imperial weights.  Also can be used
    to add fields that are similar but are labeled with different units.

    Args:
        BaseWeightForm (class): Base class for weight forms.
    """

    weight = forms.IntegerField(
        label="Weight (lb)",
        min_value=0,
    )
