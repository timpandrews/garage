from django.test import TestCase

from apps.trophies.forms import TrophiesForm


class TestTrophiesForm(TestCase):
    def test_trophies_form_valid(self):
        form = TrophiesForm({"trophies_edit": True})
        self.assertTrue(form.is_valid())

