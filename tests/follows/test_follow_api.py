from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from follows.models import Follow


class FollowTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="TestPassword123!"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="TestPassword123!"
        )

        url = reverse("token_obtain_pair")
        data = {"username": "user1", "password": "TestPassword123!"}
        response = self.client.post(url, data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_follow_user(self):
        url = reverse("follows:follow-user", kwargs={"pk": self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Follow.objects.filter(follower=self.user1, followed=self.user2).exists()
        )

    def test_unfollow_user(self):
        Follow.objects.create(follower=self.user1, followed=self.user2)

        url = reverse("follows:follow-user", kwargs={"pk": self.user2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Follow.objects.filter(follower=self.user1, followed=self.user2).exists()
        )

    def test_get_following(self):
        Follow.objects.create(follower=self.user1, followed=self.user2)

        url = reverse("follows:following")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["username"], "user2")
