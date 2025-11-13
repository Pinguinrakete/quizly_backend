from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework.test import APITestCase


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.valid_payload = {
            "username": "new_user",
            "password": "secure_password123",
            "confirmed_password": "secure_password123",
            "email": "new_user@example.com",
        }
        self.mismatch_payload = {
            "username": "user_mismatch",
            "password": "password1",
            "confirmed_password": "password2",
            "email": "mismatch@example.com",
        }
        self.existing_user = User.objects.create_user(
            username="existing", email="existing@example.com", password="password123"
        )

    def test_register_valid_user_creates_account(self):
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "User created successfully!")
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_register_with_mismatched_passwords_returns_error(self):
        response = self.client.post(self.url, self.mismatch_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirmed_password", response.data)
        self.assertIn("Passwords do not match", response.data["confirmed_password"][0])

    def test_register_with_existing_username_returns_error(self):
        payload = {
            "username": "existing",
            "password": "password123",
            "confirmed_password": "password123",
            "email": "unique_email@example.com",
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn(
            "A user with that username already exists.", response.data["username"][0]
        )

    def test_register_with_existing_email_returns_error(self):
        payload = {
            "username": "unique_user",
            "password": "password123",
            "confirmed_password": "password123",
            "email": "existing@example.com",
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("Invalid credentials.", response.data["email"][0])


class CookieTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="strongpassword123"
        )
        self.url = reverse("login")

    def test_login_success_sets_cookies(self):
        """
        Test: Successful login returns 200 and sets JWT cookies.
        """
        data = {"username": "testuser", "password": "strongpassword123"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("detail", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "testuser")

        cookies = response.cookies
        self.assertIn("access_token", cookies)
        self.assertIn("refresh_token", cookies)

        access_cookie = cookies["access_token"]
        refresh_cookie = cookies["refresh_token"]

        self.assertTrue(access_cookie["httponly"])
        self.assertTrue(refresh_cookie["httponly"])
        self.assertTrue(access_cookie["secure"])
        self.assertTrue(refresh_cookie["secure"])

    def test_login_failure_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)

    def test_login_failure_missing_fields(self):
        data = {"username": "testuser"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"][0], "This field is required.")


class CookieTokenRefreshViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.url = reverse("token_refresh")

        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.access_token = str(refresh.access_token)

    def test_refresh_token_success(self):
        self.client.cookies["refresh_token"] = self.refresh_token

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertEqual(response.data["message"], "Token refreshed")

        self.assertIn("access_token", response.cookies)
        self.assertEqual(
            response.cookies["access_token"].value, response.data["access"]
        )

    def test_refresh_token_missing(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Refresh token invalid!")

    def test_refresh_token_invalid(self):
        self.client.cookies["refresh_token"] = "invalidtoken"

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Refresh token invalid!")


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.url = reverse("logout")

    def test_logout_blacklists_refresh_token(self):
        """
        Test: After logout, the refresh token is blacklisted and cannot be used again.
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        self.client.cookies["refresh_token"] = refresh_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"],
            "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.",
        )

        blacklisted = BlacklistedToken.objects.filter(
            token__token=refresh_token
        ).exists()
        self.assertTrue(blacklisted, "Refresh token was not blacklisted after logout.")

        self.client.cookies["refresh_token"] = refresh_token
        refresh_url = reverse("token_refresh")
        refresh_response = self.client.post(refresh_url)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(refresh_response.data["detail"], "Refresh token invalid!")

    def test_logout_with_valid_refresh_token(self):
        """
        Test: Logging out with a valid refresh token deletes cookies and returns 200.
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        self.client.cookies["refresh_token"] = refresh_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"],
            "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.",
        )

        self.assertIn("refresh_token", response.cookies)
        self.assertEqual(response.cookies["refresh_token"].value, "")
        self.assertIn("access_token", response.cookies)
        self.assertEqual(response.cookies["access_token"].value, "")

    def test_logout_without_refresh_token(self):
        """
        Test: Logging out without a refresh token still returns 200 and clears cookies.
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"],
            "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.",
        )

        self.assertIn("refresh_token", response.cookies)
        self.assertEqual(response.cookies["refresh_token"].value, "")
        self.assertIn("access_token", response.cookies)
        self.assertEqual(response.cookies["access_token"].value, "")
