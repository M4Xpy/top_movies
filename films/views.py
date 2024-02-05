from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (CustomerCreationForm,
                    ActorForm, ActorSearchForm, CountryForm, CountrySearchForm)
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


class ActorListView(generic.ListView):
    model = Actor
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ActorListView, self).get_context_data(**kwargs)
        context["search_form"] = ActorSearchForm(
            initial={"full_name": self.request.GET.get("full_name", "")}
        )

        return context

    def get_queryset(self):
        queryset = Actor.objects.select_related("country").prefetch_related(
            "films_actors__genre",
        )

        full_name = self.request.GET.get("full_name")
        country_id = self.request.GET.get("country_id")
        if full_name:
            return queryset.filter(
                models.Q(name__icontains=full_name)
                | models.Q(surname__icontains=full_name)
            )
        if country_id:
            return queryset.filter(country__id=country_id)

        queryset = queryset.annotate(
            genre_count=Count("films_actors__genre", distinct=True),
            topic_count=Count("films_actors__topics", distinct=True),
        )

        return queryset


class ActorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("films:actor-list")


class ActorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Actor
    template_name = "includes/delete_confirmation.html"
    success_url = reverse_lazy("films:actor-list")


class CountryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy("films:country-list")


class CountryListView(generic.ListView):
    model = Country
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context["search_form"] = CountrySearchForm(
            initial={"name": self.request.GET.get("name", "")}
        )
        return context

    def get_queryset(self):
        queryset = Country.objects.prefetch_related(
            "films_country",
            "actors",
            "films_country__topics",
            "films_country__genre",
        )
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        queryset = queryset.annotate(
            genre_count=Count("films_country__genre", distinct=True),
            topic_count=Count("films_country__topics", distinct=True),
        )
        return queryset
