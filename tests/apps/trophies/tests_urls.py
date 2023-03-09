from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.trophies.views import trophies_edit, trophies_view, TrophiesRedirectView


class TestTrophiesUrls(SimpleTestCase):
    def test_trophies_redirect_url_is_resolved(self):
        url = reverse('trophies:trophies')
        self.assertEquals(resolve(url).func.view_class, TrophiesRedirectView)

    def test_trophies_edit_url_is_resolved(self):
        url = reverse('trophies:edit', args=[1])
        self.assertEquals(resolve(url).func, trophies_edit)

    def test_trophies_view_url_is_resolved(self):
        url = reverse('trophies:view', args=[1])
        self.assertEquals(resolve(url).func, trophies_view)