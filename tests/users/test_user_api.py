from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse("users:register")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "password2": "TestPassword123!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")
        self.assertEqual(User.objects.get().email, "test@example.com")


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPassword123!"
        )

    def test_login(self):
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "TestPassword123!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class UserProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPassword123!"
        )
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "TestPassword123!"}
        response = self.client.post(url, data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_profile(self):
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")
