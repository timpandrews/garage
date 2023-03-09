from django.test import TestCase

from apps.rides.forms import RideForm


class TestRideForms(TestCase):
    def test_ride_form_valid(self):
        form = RideForm(
            {
                "start": "01/01/2020 00:00:00",
                "ride_title": "Test Ride",
                "route": "Test Route",
                "equipment": "Test Equipment",
                "notes": "Test Notes",
                "distance": 100,
                "duration": "00:00:00",
                "elevation": 100,
                "weighted_power_avg": 100,
                "total_work": 100,
                "speed_avg": 100,
                "speed_max": 100,
                "hr_avg": 100,
                "hr_max": 100,
                "cadence_avg": 100,
                "cadence_max": 100,
                "power_avg": 100,
                "power_max": 100,
                "calories": 100,
            }
        )
        self.assertTrue(form.is_valid())

    def test_ride_form_invalid(self):
        form = RideForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 15)

