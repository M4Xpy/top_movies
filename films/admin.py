from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, Country, Genre, Actor, Film


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("genre",)
    list_filter = ("genre",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ("get_full_name",)
    list_filter = (
        "name",
        "surname",
    )


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = [
        "film_name",
        "film_year",
    ]
    search_fields = (
        "film_name",
        "film_year",
    )
    list_filter = ("film_name",)
