from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.test import APITestCase


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


class CookieTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpassword123"
        )
        self.url = reverse('login')

    def test_login_success_sets_cookies(self):
        """
        Test: Successful login returns 200 and sets JWT cookies.
        """
        data = {
            "username": "testuser",
            "password": "strongpassword123"
        }

        response = self.client.post(self.url, data, format='json')

        # --- Check status ---
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # --- Check JSON content ---
        self.assertIn("detail", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "testuser")

        # --- Check cookies ---
        cookies = response.cookies
        self.assertIn('access_token', cookies)
        self.assertIn('refresh_token', cookies)

        access_cookie = cookies['access_token']
        refresh_cookie = cookies['refresh_token']

        # Check HTTP-only and Secure flags
        self.assertTrue(access_cookie['httponly'])
        self.assertTrue(refresh_cookie['httponly'])
        self.assertTrue(access_cookie['secure'])
        self.assertTrue(refresh_cookie['secure'])

    def test_login_failure_invalid_credentials(self):
        """
        Test: Invalid password returns 401 Unauthorized.
        """
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access_token', response.cookies)
        self.assertNotIn('refresh_token', response.cookies)

    def test_login_failure_missing_fields(self):
        """
        Test: Missing fields return 401 and field-specific error messages.
        """
        data = {"username": "testuser"}  # missing password

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check that a field-specific error exists
        self.assertIn('password', response.data)
        self.assertEqual(
            response.data['password'][0],
            'This field is required.'
        )


class CookieTokenRefreshViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.url = reverse("token_refresh")

        # Generate refresh and access tokens for the test user
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.access_token = str(refresh.access_token)

    def test_refresh_token_success(self):
        # Set the refresh token in the cookie
        self.client.cookies["refresh_token"] = self.refresh_token

        response = self.client.post(self.url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response contains the new access token
        self.assertIn("access", response.data)
        self.assertEqual(response.data["message"], "Token refreshed")

        # Check that the access_token cookie is set correctly
        self.assertIn("access_token", response.cookies)
        self.assertEqual(response.cookies["access_token"].value, response.data["access"])

    def test_refresh_token_missing(self):
        # No cookie set, simulate missing refresh token
        response = self.client.post(self.url)

        # Expect 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Refresh token invalid!")

    def test_refresh_token_invalid(self):
        # Set an invalid refresh token
        self.client.cookies["refresh_token"] = "invalidtoken"

        response = self.client.post(self.url)

        # Expect 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Refresh token invalid!")


class LogoutViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.url = reverse('logout')

    def test_logout_blacklists_refresh_token(self):
        """
        Test: After logout, the refresh token is blacklisted and cannot be used again.
        """
        # Generate tokens for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Set the refresh token in cookies and access token in Authorization header
        self.client.cookies['refresh_token'] = refresh_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Send POST request to logout endpoint
        response = self.client.post(self.url)

        # Assert logout response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['detail'], "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.")

        # Assert that the refresh token is blacklisted
        blacklisted = BlacklistedToken.objects.filter(token__token=refresh_token).exists()
        self.assertTrue(blacklisted, "Refresh token was not blacklisted after logout.")

        # Optional: verify that using the same refresh token fails
        self.client.cookies['refresh_token'] = refresh_token
        refresh_url = reverse("token_refresh")
        refresh_response = self.client.post(refresh_url)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(refresh_response.data['detail'], "Refresh token invalid!")

    def test_logout_with_valid_refresh_token(self):
        """
        Test: Logging out with a valid refresh token deletes cookies and returns 200.
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        self.client.cookies['refresh_token'] = refresh_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['detail'], "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.")

        # Assert cookies are deleted
        self.assertIn('refresh_token', response.cookies)
        self.assertEqual(response.cookies['refresh_token'].value, '')
        self.assertIn('access_token', response.cookies)
        self.assertEqual(response.cookies['access_token'].value, '')

    def test_logout_without_refresh_token(self):
        """
        Test: Logging out without a refresh token still returns 200 and clears cookies.
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Set only access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['detail'], "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.")

        # Assert cookies are deleted even if no refresh token was present
        self.assertIn('refresh_token', response.cookies)
        self.assertEqual(response.cookies['refresh_token'].value, '')
        self.assertIn('access_token', response.cookies)
        self.assertEqual(response.cookies['access_token'].value, '')