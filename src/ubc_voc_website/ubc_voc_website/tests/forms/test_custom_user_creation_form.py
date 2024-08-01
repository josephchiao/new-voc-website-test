from django.test import TestCase
from django.contrib.auth import get_user_model
from ubc_voc_website.forms import CustomUserCreationForm
from membership.models import Profile
import datetime

class CustomUserCreationFormTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.valid_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'pronouns': 'Test/User',
            'phone': '(111)-111-1111',
            'student_number': '12345678',
            'birthdate': '2000-01-01'
        }

    def test_valid_data(self):
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        data = self.valid_data.copy()
        del data['email']
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = "invalid-email"
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_password1(self):
        data = self.valid_data.copy()
        del data['password1']
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_password2(self):
        data = self.valid_data.copy()
        del data['password2']
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_mismatched_passwords(self):
        data = self.valid_data.copy()
        data['password2'] = 'wrong-password'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_firstname(self):
        data = self.valid_data.copy()
        del data['first_name']
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_lastname(self):
        data = self.valid_data.copy()
        del data['last_name']
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_phone(self):
        data = self.valid_data.copy()
        del data['phone']
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_save(self):
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(self.User.objects.count(), 1)
        self.assertEqual(self.User.objects.first().email, self.valid_data['email'])

        self.assertEqual(Profile.objects.count(), 1)
        profile = Profile.objects.first()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.first_name, self.valid_data['first_name'])
        self.assertEqual(profile.last_name, self.valid_data['last_name'])
        self.assertEqual(profile.pronouns, self.valid_data['pronouns'])
        self.assertEqual(profile.phone, self.valid_data['phone'])
        self.assertEqual(profile.student_number, self.valid_data['student_number'])
        self.assertEqual(profile.birthdate, datetime.datetime.strptime(self.valid_data['birthdate'], '%Y-%m-%d').date())
        self.assertIsNone(profile.blurb)

    def test_commit_false(self):
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)

        self.assertEqual(self.User.objects.count(), 0)

        user.save()
        self.assertEqual(self.User.objects.count(), 1)

