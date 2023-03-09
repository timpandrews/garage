from django.contrib.auth.views import PasswordChangeView
from django.test import SimpleTestCase # use simple test case when not using database
from django.urls import resolve, reverse

from apps.garage.views import ActivateAccount, SignUpView, landing, profile


class TestUrls(SimpleTestCase):
    def test_landing_url_is_resolved(self):
        url = reverse('landing')
        self.assertEquals(resolve(url).func, landing)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, landing)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_activate_url_is_resolved(self):
        url = reverse('activate', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, ActivateAccount)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_change_password_url_is_resolved(self):
        url = reverse('change_password')
        self.assertEquals(resolve(url).func.view_class, PasswordChangeView)