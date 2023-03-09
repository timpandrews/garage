from django.test import TestCase

class SimpleTest(TestCase):
    def test_one_equals_one(self):
        self.assertEqual(1, 1)  