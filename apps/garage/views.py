import json
import os
from datetime import datetime

import fitdecode
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView, View

from .helper import get_next
from .forms import SignUpForm, UpdateProfileForm, UpdateUserForm
from .tokens import account_activation_token
from .models import Doc


def landing(response):
    return render(response, "garage/landing.html", {})


class ToolsView(LoginRequiredMixin, TemplateView):
    template_name = "garage/tools.html"

# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('landing')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('landing')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile )

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def parse_fit_file(request):
    print("Parse Fit File")
    file = 'test.fit'
    cwd = os.getcwd()
    path = os.path.join(cwd, 'data')
    file = os.path.join(path, file)

    # one pass through the file to get the names of the frames
    data_types = []
    with fitdecode.FitReader(file) as fit:
        fit_file = {}
        for i, frame in enumerate(fit):
            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                if frame.name not in data_types:
                    fit_file[frame.name] = ""
                    data_types.append(frame.name)

    # loop through the fit file again for each data_type
    for data_type in data_types:
        data = []
        with fitdecode.FitReader(file) as fit:
            for i, frame in enumerate(fit):
                if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == data_type:
                    row = {}
                    for field in frame:
                        # TODO do I need to convert datatime to string if I don't convert to JSON?
                        if type(field.value) == datetime:
                            row[field.name] = field.value.strftime('%Y-%m-%d %H:%M:%S %Z')
                        else:
                            row[field.name] = field.value
                    data.append(row)
            fit_file[data_type] = data

    fit_file_json = json.dumps(fit_file)
    # print(fit_file_json)

    print(fit_file["file_id"][0]["manufacturer"])


    doc_data = {}
    doc_data['start'] = fit_file["session"][0]["start_time"]
    doc_data['notes'] = "test notes"
    doc_data['hr'] = 150
    doc_data['fit_file'] = fit_file

    doc_values = {}
    doc_values['user'] = request.user
    doc_values['doc_type'] = 'test'
    doc_values['doc_date'] = datetime.now()
    doc_values['data'] = doc_data
    Doc.objects.create(**doc_values)

    return redirect(reverse('tools'))