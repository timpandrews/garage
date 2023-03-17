from django.test import TestCase

from apps.hp.forms import GenericHPForm, WeightHPForm, BPHPForm

class GenericHPFormTest(TestCase):
    def test_generic_hp_form_valid(self):
        form = GenericHPForm({
            "type": "other",
            "data": '{"test":"data"}'
        })
        self.assertTrue(form.is_valid())

    def test_generic_hp_form_invalid(self):
        form = GenericHPForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class WeightHPFormTest(TestCase):
    def test_weight_hp_form_valid(self):
        form = WeightHPForm({
            "type": "weight",
            "weight": 100,
        })
        self.assertTrue(form.is_valid())

    def test_weight_hp_form_invalid(self):
        form = WeightHPForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class BPHPFormTest(TestCase):
    def test_bp_hp_form_valid(self):
        form = BPHPForm({
            "type": "bp",
            "bp_STOL": 100,
            "bp_DTOL": 100,
        })
        self.assertTrue(form.is_valid())

    def test_bp_hp_form_invalid(self):
        form = BPHPForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
