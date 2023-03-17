from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.kudos.views import kudos


class TestKudosURL(SimpleTestCase):
    def test_kudos_url_is_resolved(self):
        url = reverse("kudos:kudos")
        self.assertEquals(resolve(url).func, kudos)
