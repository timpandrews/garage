from django.forms import ModelForm
from .models import Doc

class AddNewRide(ModelForm):

    class Meta:
        model = Doc
        fields = "__all__"

