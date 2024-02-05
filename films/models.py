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
