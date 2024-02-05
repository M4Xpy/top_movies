from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicTest(TestCase):
    def test_actor_create_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("films:actor-create")).status_code, 200
        )

    def test_country_create_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("films:country-create")).status_code, 200
        )

    def test_topic_create_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("films:topic-create")).status_code, 200
        )

    def test_genre_create_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("films:genre-create")).status_code, 200
        )

    def test_movie_create_login_required(self):
        self.assertNotEqual(
            self.client.get(reverse("films:movie-create")).status_code, 200
        )


class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_movie_create_request_status_code(self):
        self.assertEqual(
            self.client.get(reverse("films:movie-create")).status_code, 200
        )

    def test_actor_create_request_status_code(self):
        self.assertEqual(
            self.client.get(reverse("films:actor-create")).status_code, 200
        )

    def test_country_create_request_status_code(self):
        self.assertEqual(
            self.client.get(reverse("films:country-create")).status_code, 200
        )

    def test_topic_create_request_status_code(self):
        self.assertEqual(
            self.client.get(reverse("films:topic-create")).status_code, 200
        )

    def test_genre_create_request_status_code(self):
        self.assertEqual(
            self.client.get(reverse("films:genre-create")).status_code, 200
        )
