from django.test import TestCase

from apps.dashboard.forms import DBMonthForm


class DBMonthFormTest(TestCase):
    def text_DBMonthForm_valid(self):
        form = DBMonthForm(
            {
                "start_year": "01/01/2020",
                "end_year": "01/01/2022",
            }
        )
        self.assertTrue(form.is_valid())

    def test_DBMonthForm_invalid(self):
        form = DBMonthForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)