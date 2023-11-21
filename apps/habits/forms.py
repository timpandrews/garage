from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from datetime import datetime

from apps.garage.models import Doc, Profile


class HabitForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Store the user in the form for later use

        self.fields["date"] = forms.DateField(
            required=True,
            widget=DatePickerInput(attrs={"class": "form-control"}),
            initial=datetime.today(),
        )

        habits = Profile.objects.filter(user=user).values("habits").first()["habits"]
        HABITS = [('','Please select one of your good habits')]
        for key, habit in habits.items():
            habit_tuple = (habit, habit)
            HABITS.append(habit_tuple)
        print("HABITS", HABITS)
        self.fields["good_habits"] = forms.ChoiceField(
            choices=HABITS,
            help_text="""Please select one of your good habits that you have
                        performed.  These habits are defined in your profile.""",
        )


    class Meta:
        model = Doc
        exclude = "__all__"
        fields = []
