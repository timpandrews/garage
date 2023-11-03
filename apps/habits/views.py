from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from apps.garage.models import Doc, Profile

from .forms import HabitForm

"""
Place holder view for managing habits.  For now it simply displays
the list of habits that is defined in the habits field of the Profile model.

It will eventually allow the user to add, delete, and modify habits.

Returns:
    _type_: _description_
"""
class ManageHabits(LoginRequiredMixin, TemplateView):
    template_name = "habits/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habits = Profile.objects.filter(user=self.request.user).values("habits").first()
        context["habits"] = habits["habits"]
        # print(habits)
        return context


class HabitBaseView(View):
    model = Doc
    success_url = reverse_lazy('habits:list')


class HabitListView(LoginRequiredMixin, HabitBaseView, ListView):
    template_name = 'habits/habits_list.html'
    context_object_name = 'habits'
    paginate_by = 20

    def get_queryset(self):
        hps = self.model.objects.order_by("-id").filter(
            doc_type="habit", user=self.request.user, active=True
        )

        return hps


class HabitDetailView(LoginRequiredMixin, HabitBaseView, DetailView):
    fields = "__all__"
    template_name = "habits/hp_detail.html"


class HabitCreateView(LoginRequiredMixin, HabitBaseView, CreateView):
    form_class = HabitForm
    template_name = 'habits/habits_form.html'

    """ Used to pass the current user to the form """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["choices"] = Profile.objects.filter(user=self.request.user).values("habits").first()["habits"]
    #     print("context: ", context)
    #     return context



class HabitUpdateView(LoginRequiredMixin, HabitBaseView, UpdateView):
    form_class = HabitForm
    template_name = 'habits/habits_form.html'


class HabitDeleteView(LoginRequiredMixin, HabitBaseView, DeleteView):
    template_name = 'habits/task_confirm_delete.html'


class HabitUpdateView(LoginRequiredMixin, HabitBaseView, UpdateView):
    form_class = HabitForm
    template_name = "habits/habits_form.html"