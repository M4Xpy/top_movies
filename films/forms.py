from django.contrib.auth.forms import UserCreationForm
from django import forms

from films.models import Film, Customer, Actor, Genre, Country, Rate, Topic


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
