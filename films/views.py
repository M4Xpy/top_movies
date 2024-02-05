from django.shortcuts import render

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
