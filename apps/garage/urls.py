from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (ActivateAccount, SignUpView, ToolsView, landing, profile)

urlpatterns = [
    path('', landing, name='landing'),
    path('', landing, name='home'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('accounts/profile/', profile, name='profile'),
    path(
        'accounts/change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
]