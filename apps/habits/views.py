from django.views.generic import TemplateView

class Habits(TemplateView):
    template_name = "habits/manage.html"
