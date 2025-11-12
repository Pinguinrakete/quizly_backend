from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.valid_payload = {
            "username": "new_user",
            "password": "secure_password123",
            "confirmed_password": "secure_password123",
            "email": "new_user@example.com"
        }
        self.mismatch_payload = {
            "username": "user_mismatch",
            "password": "password1",
            "confirmed_password": "password2",
            "email": "mismatch@example.com"
        }
        # Existing user for duplicate tests
        self.existing_user = User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="password123"
        )

    def test_register_valid_user_creates_account(self):
        """✅ A new user is successfully created."""
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], "User created successfully!")
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_register_with_mismatched_passwords_returns_error(self):
        """❌ If passwords do not match, a 400 error is returned."""
        response = self.client.post(self.url, self.mismatch_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmed_password', response.data)
        self.assertIn('Passwords do not match', response.data['confirmed_password'][0])

    def test_register_with_existing_username_returns_error(self):
        """❌ If the username already exists, an error is returned."""
        payload = {
            "username": "existing",
            "password": "password123",
            "confirmed_password": "password123",
            "email": "unique_email@example.com"
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn(
            'A user with that username already exists.',
            response.data['username'][0]
        )

    def test_register_with_existing_email_returns_error(self):
        """❌ If the email already exists, an error is returned."""
        payload = {
            "username": "unique_user",
            "password": "password123",
            "confirmed_password": "password123",
            "email": "existing@example.com"
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('Invalid credentials.', response.data['email'][0])