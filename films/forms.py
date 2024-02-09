from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator

from films.models import Film, Customer, Actor, Country


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ("name", "surname", "country")


class ActorSearchForm(forms.Form):
    full_name = forms.CharField(
        max_length=99,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search  actor  by  name  or(and)  surname",
                "style": "width: 400px;",
            }
        ),
    )


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("name",)


class CountrySearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search  country  by  name",
                "style": "width: 400px;",
            }
        ),
    )


class GenreSearchForm(forms.Form):
    genre = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search  actor  by  genre",
                "style": "width: 400px;",
            }
        ),
    )


class FilmForm(forms.ModelForm):
    film_year = forms.IntegerField(
        validators=[MinValueValidator(1900),
                    MaxValueValidator(datetime.now().year)],
        required=False,
    )

    class Meta:
        model = Film
        fields = "__all__"


class MovieSearchForm(forms.Form):
    film_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search  movie  by  name",
                "style": "width: 400px;",
            }
        ),
    )


class TopicSearchForm(forms.Form):
    topic = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search  actor  by  topic",
                "style": "width: 400px;",
            }
        ),
    )
