from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.trophies.views import (TrophiesRedirectView, trophies_edit,
                                 trophies_share, trophies_view)


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

    def test_trophies_share_root_url_is_resolved(self):
        url = reverse('trophies:share_root', args=['username'])
        self.assertEquals(resolve(url).func, trophies_share)

    def test_username_share_trophies_url_is_resolved(self):
        url = reverse('trophies:share_trophies', args=['username'])
        self.assertEquals(resolve(url).func, trophies_share)