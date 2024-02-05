from django.test import TestCase
from django.urls import reverse

from films.forms import (
    CustomerCreationForm,
    GenreSearchForm,
    TopicSearchForm,
    CountrySearchForm,
    ActorSearchForm,
    MovieSearchForm,
)
from films.models import Genre, Topic, Country, Actor, Film


class FormsTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        self.form = CustomerCreationForm(data=self.form_data)

    def test_customer_creation_form_with_all_names_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)


class SearchTests(TestCase):
    test_password = "1234567890"

    def setUp(self):
        self.genre_response = self.client.get(
            reverse("films:genre-list"), {"genre": "test_genre"}
        )
        self.topic_response = self.client.get(
            reverse("films:topic-list"), {"name": "test_topic"}
        )
        self.country_response = self.client.get(
            reverse("films:country-list"), {"name": "test_country"}
        )
        self.actor_response = self.client.get(
            reverse("films:actor-list"), {"name": "test_actor"}
        )
        self.movie_response = self.client.get(
            reverse("films:movie-list"),
            {
                "film_name": "test_movie",
            },
        )

    def test_search_genre_by_name_status_code_is_200(self):
        self.assertEqual(self.genre_response.status_code, 200)

    def test_search_genre_by_name_form_instance_is_created(self):
        self.assertIsInstance(
            self.genre_response.context["search_form"],
            GenreSearchForm,
        )

    def test_search_genre_by_name_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.genre_response.context["object_list"],
            Genre.objects.filter(genre__icontains="test_genre"),
        )

    def test_search_topic_by_name_status_code_is_200(self):
        self.assertEqual(self.topic_response.status_code, 200)

    def test_search_topic_by_name_form_instance_is_created(self):
        self.assertIsInstance(
            self.topic_response.context["search_form"],
            TopicSearchForm,
        )

    def test_search_topic_by_name_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.topic_response.context["object_list"],
            Topic.objects.filter(name__icontains="test_topic"),
        )

    def test_search_country_by_name_status_code_is_200(self):
        self.assertEqual(self.country_response.status_code, 200)

    def test_search_country_by_name_form_instance_is_created(self):
        self.assertIsInstance(
            self.country_response.context["search_form"],
            CountrySearchForm,
        )

    def test_search_country_by_name_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.country_response.context["object_list"],
            Country.objects.filter(name__icontains="test_country"),
        )

    def test_search_actor_by_name_status_code_is_200(self):
        self.assertEqual(self.actor_response.status_code, 200)

    def test_search_actor_by_name_form_instance_is_created(self):
        self.assertIsInstance(
            self.actor_response.context["search_form"],
            ActorSearchForm,
        )

    def test_search_actor_by_name_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.actor_response.context["object_list"],
            Actor.objects.filter(name__icontains="test_actor"),
        )

    def test_search_movie_by_name_status_code_is_200(self):
        self.assertEqual(self.movie_response.status_code, 200)

    def test_search_movie_by_name_form_instance_is_created(self):
        self.assertIsInstance(
            self.movie_response.context["search_form"],
            MovieSearchForm,
        )

    def test_search_movie_by_name_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.movie_response.context["object_list"],
            Film.objects.filter(film_name__icontains="test_movie"),
        )
