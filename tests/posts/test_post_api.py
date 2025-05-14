from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from posts.models import Post, Like, Comment


class PostTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPassword123!"
        )

        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "TestPassword123!"}
        response = self.client.post(url, data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.post = Post.objects.create(author=self.user, content="Test post content")

    def test_create_post(self):
        url = reverse("posts:post-create")
        data = {
            "content": "New post content",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(
            Post.objects.filter(content="New post content").first().author, self.user
        )

    def test_get_post_detail(self):
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Test post content")
        self.assertEqual(response.data["author"]["username"], "testuser")

    def test_update_post(self):
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        data = {"content": "Updated content"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, "Updated content")

    def test_delete_post(self):
        url = reverse("posts:post-detail", kwargs={"pk": self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)


class LikeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPassword123!"
        )

        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "TestPassword123!"}
        response = self.client.post(url, data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.post = Post.objects.create(author=self.user, content="Test post content")

    def test_like_post(self):
        url = reverse("posts:like-post", kwargs={"pk": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.post)

        url = reverse("posts:like-post", kwargs={"pk": self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())


class CommentTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="TestPassword123!"
        )

        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "TestPassword123!"}
        response = self.client.post(url, data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.post = Post.objects.create(author=self.user, content="Test post content")

    def test_add_comment(self):
        url = reverse("posts:post-comments", kwargs={"pk": self.post.id})
        data = {"content": "Test comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, "Test comment")

    def test_get_comments(self):
        Comment.objects.create(user=self.user, post=self.post, content="Test comment")

        url = reverse("posts:post-comments", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["content"], "Test comment")
