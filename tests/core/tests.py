from django.conf import settings
from django.test import TestCase
from django.contrib.auth.password_validation import validate_password


class ConfigTest(TestCase):
    def test_secret_key_strength(self):
        self.assertGreaterEqual(len(settings.SECRET_KEY), 50)
        self.assertIsNone(validate_password(settings.SECRET_KEY))

    # tests for other settings go here
    



