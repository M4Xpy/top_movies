from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Country(models.Model):
    name = models.CharField(max_length=63)
    flag = models.ImageField(upload_to="country_flags/", null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.genre


class Actor(models.Model):
    name = models.CharField(max_length=63)
    surname = models.CharField(max_length=63)
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="actors",
    )

    class Meta:
        ordering = ("name", "surname",)

    def get_full_name(self):
        return f" {self.name} {self.surname} "

    def __str__(self):
        return f"{self.name} {self.surname}"


class Film(models.Model):
    film_year = models.IntegerField(
        blank=True,
        null=True,
    )
    film_name = models.CharField(
        max_length=63,
    )
    country = models.ManyToManyField(
        Country,
        blank=True,
        related_name="films_country",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="films_genre",
    )
    actors = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="films_actors",
    )
    topics = models.ManyToManyField(
        Topic,
        blank=True,
        related_name="films_topics"
    )

    class Meta:
        ordering = ("film_name", "film_year",)

    def get_average_rate(self):
        rates = self.film_rates.all()
        len_rates = len(rates)
        if rates:
            return f"{round(sum(rate.rating for rate in rates) / len_rates,
                            2)} / {len_rates}"
        return 0.0

    def __str__(self):
        return f"({self.film_year}) {self.film_name}"


class Rate(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 related_name="film_rates",
                                 )
    rating = models.IntegerField(default=0)
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name="film_rates",
                             )

    def __str__(self):
        return f"{self.rating}"
