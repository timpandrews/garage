from django.test import TestCase

from apps.garage.forms import SignUpForm, UpdateUserForm, UpdateProfileForm


class SignUpFormTest(TestCase):
    def test_SignUpForm_valid(self):
        form = SignUpForm(
            {
                'username': 'testuser',
                'first_name': 'test',
                'last_name': 'user',
                'email': 'testuser@test.com',
                'password1': 'notsimilar123',
                'password2': 'notsimilar123'
            }
        )
        self.assertTrue(form.is_valid())

    def test_SignUpForm_invalid(self):
        form = SignUpForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class UpdateUserFormTest(TestCase):
    def test_UpdateUserForm_valid(self):
        form = UpdateUserForm(
            {
                'username': 'testuser',
                'first_name': 'test',
                'last_name': 'user',
                'email': 'testemail@emal.com',
            }
        )
        self.assertTrue(form.is_valid())

    def test_UpdateUserForm_invalid(self):
        form = UpdateUserForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class UpdateProfileFormTest(TestCase):
    def test_UpdateProfileForm_valid(self):
        form = UpdateProfileForm(
            {
                'image': 'image.jpg',
                'bio': 'This is a test bio',
            }
        )
        self.assertTrue(form.is_valid())

    def test_UpdateProfileForm_invalid(self):
        form = UpdateProfileForm({
            'birth_date': 'bad date',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)