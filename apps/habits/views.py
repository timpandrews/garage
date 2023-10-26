from django.views.generic import TemplateView
from apps.garage.models import Profile


class Habits(TemplateView):
    template_name = "habits/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habits = Profile.objects.filter(user=self.request.user).values("habits").first()
        context["habits"] = habits["habits"]
        # print(habits)
        return context
