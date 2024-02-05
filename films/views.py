from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (CustomerCreationForm,
                    ActorForm)
from .models import (
    Customer,
    Film,
    Country,
    Actor,
    Genre,
    Rate,
    Commentary,
    Topic,
)


def index(request):
    """View function for the home page of the site."""

    num_customers = Customer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_customers": num_customers,
        "num_visits": num_visits + 1,
        "num_movies": Film.objects.count(),
        "num_actors": Actor.objects.count(),
        "num_countries": Country.objects.count(),
        "num_genres": Genre.objects.count(),
        "num_topics": Topic.objects.count(),
        "num_commentaries": Commentary.objects.count(),
    }

    return render(request, "films/index.html", context=context)


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    form_class = CustomerCreationForm


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    success_url = reverse_lazy("")


class ActorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("films:actor-list")
