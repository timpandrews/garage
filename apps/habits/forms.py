from django import forms

from apps.garage.models import Doc, Profile

CHOICES = (
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third'),
)

# class HabitForm(forms.ModelForm):
#     class Meta:
#         model = Doc
#         exclude = "__all__"
#         fields = []

#     options = forms.MultipleChoiceField(
#         choices=CHOICES)

class HabitForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Store the user in the form for later use
        habits = Profile.objects.filter(user=user).values("habits").first()["habits"]
        HABITS = []
        for key, habit in habits.items():
            habit_tuple = (habit, habit)
            HABITS.append(habit_tuple)
        self.fields['good_habits'] = forms.MultipleChoiceField(
            choices=HABITS, widget=forms.CheckboxSelectMultiple,
        )

    class Meta:
        model = Doc
        exclude = "__all__"
        fields = []



