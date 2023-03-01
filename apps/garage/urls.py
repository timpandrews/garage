from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ActivateAccount, ProfileView, SignUpView, landing

urlpatterns = [
    path('', landing, name='landing'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path(
        'change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),                                              
]