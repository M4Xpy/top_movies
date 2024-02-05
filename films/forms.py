from django.contrib.auth.forms import UserCreationForm

from films.models import Film, Customer, Actor, Genre, Country, Rate, Topic


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )
