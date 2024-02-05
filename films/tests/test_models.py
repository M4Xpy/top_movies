from django.contrib.auth import get_user_model
from django.test import TestCase

from films.models import Country, Actor, Topic, Genre, Film


class ModelsTests(TestCase):
    username = "test_user"
    password = "test_password"

    def setUp(self):
        self.country = Country.objects.create(name="test_country")
        self.actor = Actor.objects.create(name="test", surname="actor")
        self.topic = Topic.objects.create(name="test_topic")
        self.genre = Genre.objects.create(genre="test_genre")
        self.movie = Film.objects.create(film_year=1999,
                                         film_name="test_movie")
        self.customer = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="John",
            last_name="Doe",
        )

    def test_country_str(self):
        self.assertEqual(str(self.country), f"{self.country.name}")

    def test_actor_str(self):
        self.assertEqual(str(self.actor),
                         f"{self.actor.name} {self.actor.surname}")

    def test_topic_str(self):
        self.assertEqual(str(self.topic), f"{self.topic.name}")

    def test_genre_str(self):
        self.assertEqual(str(self.genre), f"{self.genre.genre}")

    def test_movie_str(self):
        self.assertEqual(
            str(self.movie), f"({self.movie.film_year}) {self.movie.film_name}"
        )

    def test_customer_username(self):
        self.assertEqual(self.customer.username, self.username)

    def test_customer_password(self):
        self.assertTrue(self.customer.check_password(self.password))
